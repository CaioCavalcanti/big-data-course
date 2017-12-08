<!DOCTYPE html>
<html>
    <head>
        <title>My Blog with Python and MongoDB</title>
    </head>
    <body>
        <h1>My Blog with Python and MongoDB</h1>
        %for post in posts:
        <article class="post">
            <header class="post-title">
                <a href="/post/{{ post['permalink'] }}">{{ post['title'] }}</a>
            </header>
            <p class="post-info">
                <h4>{{ post['author'] }}</h4>
                <small>{{ post['date'] }}</small>
            </p>
            <p class="post-body">
                {{ post['body'] }}
            </p>
            <p class="post-tags">
            </p>
            <footer class="post-footer">
                <label class="post-comments">
                    {{ len(post['comments']) }} comments
                </label>
                <label class="post-tags">
                    %if('tags' in post and len(post['tags']) > 0):
                        %for tag in post['tags']:
                        <a class="post-tag" href="/tag/{{tag}}">{{ tag }}</a>
                        %end
                    %end
                </label>
            </footer>
        </article>
        %end
    </body>
</html>