from flask import Blueprint, render_template, request

"""
     スタート画面
     グループ名の入力
"""

start_bp = Blueprint('start', __name__)

@start_bp.route('/start', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        group_name = request.form["group_name"]
        return render_template('anser_question.html', group_name=group_name)
    return render_template('start.html')