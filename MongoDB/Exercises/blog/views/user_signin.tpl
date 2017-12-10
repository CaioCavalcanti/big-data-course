<!doctype HTML>
<html>
    <head>
        <title>Blog - Singin</title>
    </head>
    <body>
        <a href="/">Blog Home</a>
        <h1>Signup</h1>
        <form action="/signin" method="POST">
            %if error:
            <div class="error">
                {{ error }}
            </div>
            %end
            <div class="input-field">
                <input type="email" id="email" name="email" placeholder="Name" class="validate" value="{{ email }}" required />
                <label for="email">Email *</label>
            </div>
            <div class="input-field">
                <input type="password" id="password" name="password" placeholder="Name" class="validate" value="{{ password }}" required />
                <label for="password">Password *</label>
            </div>
            <div>
                <input type="submit" value="Signin" class="waves-effect waves-light btn" />
            </div>
        </form>
    </body>
</html>