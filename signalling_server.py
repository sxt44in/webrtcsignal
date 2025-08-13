from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)
sessions = {}

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/offer/<session_code>', methods=['POST'])
def post_offer(session_code):
    try:
        data = request.json
        logger.debug(f"Received POST /offer/{{session_code}}: {{data}}")
        if not data or 'sdp' not in data or 'type' not in data:
            logger.error(f"Invalid data in POST /offer/{{session_code}}")
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
        if session_code not in sessions:
            sessions[session_code] = {}
        sessions[session_code]['offer'] = data['sdp']
        sessions[session_code]['offer_type'] = data['type']
        logger.info(f"Stored offer for session {{session_code}}")
        return jsonify({'status': 'ok'})
    except Exception as e:
        logger.error(f"Error in post_offer for session {{session_code}}: {{e}}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/offer/<session_code>', methods=['GET'])
def get_offer(session_code):
    try:
        logger.debug(f"Received GET /offer/{{session_code}}")
        if session_code in sessions and 'offer' in sessions[session_code]:
            return jsonify({
                'sdp': sessions[session_code]['offer'],
                'type': sessions[session_code]['offer_type']
            })
        logger.warning(f"No offer found for session {{session_code}}")
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        logger.error(f"Error in get_offer for session {{session_code}}: {{e}}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/answer/<session_code>', methods=['POST'])
def post_answer(session_code):
    try:
        data = request.json
        logger.debug(f"Received POST /answer/{{session_code}}: {{data}}")
        if not data or 'sdp' not in data or 'type' not in data:
            logger.error(f"Invalid data in POST /answer/{{session_code}}")
            return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
        if session_code not in sessions:
            sessions[session_code] = {}
        sessions[session_code]['answer'] = data['sdp']
        sessions[session_code]['answer_type'] = data['type']
        logger.info(f"Stored answer for session {{session_code}}")
        return jsonify({'status': 'ok'})
    except Exception as e:
        logger.error(f"Error in post_answer for session {{session_code}}: {{e}}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/answer/<session_code>', methods=['GET'])
def get_answer(session_code):
    try:
        logger.debug(f"Received GET /answer/{{session_code}}")
        if session_code in sessions and 'answer' in sessions[session_code]:
            return jsonify({
                'sdp': sessions[session_code]['answer'],
                'type': sessions[session_code]['answer_type']
            })
        logger.warning(f"No answer found for session {{session_code}}")
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        logger.error(f"Error in get_answer for session {{session_code}}: {{e}}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting server on port {{port}}")
    app.run(host='0.0.0.0', port=port, debug=False)  # Disable debug for production
