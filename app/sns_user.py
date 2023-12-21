# ログインなどユーザーに関する処理をまとめた
import crud

# ログインを試行する --- (*3)
def try_login(form):
    user = form.get('user', '')
    password = form.get('pw', '')
    # パスワードチェック
    if check_username_email(user,password):
        return True
    else
        return False
