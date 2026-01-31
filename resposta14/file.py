from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Transaction, db
import os
from pathlib import Path

app = Flask(__name__)
ALLOWED_UPLOAD_DIR = "/files"

# Rota para download de comprovante
# Exemplo de chamada: GET /api/v1/transactions/1099/receipt
@app.route('/api/v1/transactions/<int:transaction_id>/receipt',
methods=['GET'])
@jwt_required()
def download_receipt(transaction_id):
    try:
        # Recupera o ID do usuário logado (ex: 55)
        current_user_id = get_jwt_identity()
        
        # Busca a transação no banco de dados pelo ID fornecido na URL
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transação não encontrada"}), 404
        
        # CORREÇÃO 1: Valida se o usuário é o proprietário da transação
        # Previne que um usuário acesse comprovantes de outro usuário
        # Retorna 404 para não revelar a existência da transação
        if transaction.user_id != current_user_id:
            return jsonify({"error": "Transação não encontrada"}), 404
        
        # CORREÇÃO 2: Valida o caminho do arquivo (previne Path Traversal)
        # Garante que o caminho resolvido fica dentro do diretório permitido
        file_path = Path(transaction.receipt_path).resolve()
        allowed_path = Path(ALLOWED_UPLOAD_DIR).resolve()
        
        if not str(file_path).startswith(str(allowed_path)):
            return jsonify({"error": "Arquivo inválido"}), 400
        
        # CORREÇÃO 3: Valida se o arquivo existe e é um PDF
        # Previne acesso a arquivos inexistentes ou com extensão diferente
        if not file_path.exists() or not file_path.suffix.lower() == '.pdf':
            return jsonify({"error": "Arquivo não encontrado ou inválido"}), 404
        
        # Retorna o arquivo PDF do comprovante
        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=f"receipt_{transaction_id}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": "Erro interno do servidor"}), 500
