<!doctype HTML>
<html <head>
<title>
    Blog - {{ post['title'] }}
</title>
</head>

<body>
    <a href="/">Blog Home</a>

    <article class="post">
        <header class="post-title">{{ post['title'] }}</header>
        <p class="post-info">
            <h4>{{ post['author'] }}</h4>
            <small>{{ post['date'] }}</small>
            <label class="post-tags">
                %if('tags' in post and len(post['tags']) > 0):
                    %for tag in post['tags']:
                    <a class="post-tag" href="/tag/{{tag}}">{{ tag }}</a>
                    %end
                %end
            </label>
        </p>
        <p class="post-body">
            {{ post['body'] }}
        </p>
        <footer class="post-footer">
            <div class="post-comments">
                <h3>{{ len(post['comments']) }} comments</h3>
                %for comment in post['comments']:
                <div class="post-comment">
                    <a href="mailto:{{ comment['author'] }}">{{ comment['author'] }}</a>
                    <small>{{ comment['date'] }}</small>
                    <p>{{ comment['message'] }}</p>
                </div>
                %end
            </div>
        </footer>
    </article>
</body>

</html>