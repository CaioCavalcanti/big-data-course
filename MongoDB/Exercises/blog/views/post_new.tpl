<!doctype HTML>
<html>
    <head>
        <title>Blog - New post</title>
    </head>
    <body>
        <a href="/">Blog Home</a>
        <form action="/newpost" method="POST">
            <h2>Title</h2>
            <input type="text" name="subject" size="120" value="{{subject}}"><br>
            <h2>Body<h2>
            <textarea name="body" cols="120" rows="20">{{body}}</textarea><br>
            <h2>Tags</h2>
            <small>Comma separated</small>
            <input type="text" name="tags" size="120" value="{{tags}}">
            <input type="submit" value="Submit">
        </form>
    </body>
</html>