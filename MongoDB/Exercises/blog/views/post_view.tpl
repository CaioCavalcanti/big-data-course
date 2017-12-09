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
                <form action="/comment" method="POST" class="new-comment">
                    %if errors:
                    <div class="">
                        <p>{{ errors }}</p>
                    </div>
                    %end
                    <input type="hidden" name="permalink" value="{{ post['permalink'] }}" />
                    <div class="input-field">
                        <input type="text" id="name" name="name" placeholder="Name" class="validate" value="{{ comment['author'] }}" required />
                        <label for="name">Name *</label>
                    </div>
                    <div class="input-field">
                        <input type="email" id="email" name="email" placeholder="Email" class="validate" value="{{ comment['email'] }}" required />
                        <label for="email">Email *</label>
                    </div>
                    <div class="input-field">
                        <textarea rows="4" id="message" name="message" placeholder="Message" class="validate" value="{{ comment['message'] }}" required></textarea>
                        <label for="message">Message *</label>
                    </div>
                    <div>
                        <input type="submit" value="Submit" class="waves-effect waves-light btn" />
                    </div>
                </form>
                %for comment in post['comments']:
                <div class="post-comment">
                    <a href="mailto:{{ comment['email'] }}">{{ comment['author'] }}</a>
                    <small>{{ comment['date'] }}</small>
                    <p>{{ comment['message'] }}</p>
                </div>
                %end
            </div>
        </footer>
    </article>
</body>

</html>