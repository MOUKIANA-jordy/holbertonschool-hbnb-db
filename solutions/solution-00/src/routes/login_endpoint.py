 @app.route('/login', methods=['POST'])
 def login():
     username = request.json.get('username', None)
     password = request.json.get('password', None)
     user = User.query.filter_by(username=username).first()
     if user and bcrypt.check_password_hash(user.password, password):
         access_token = create_access_token(identity=username)
         return jsonify(access_token=access_token), 200
     return 'Wrong username or password', 401
