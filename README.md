# citizenline
Open source project for citizen participation tools


Issues:
1. Data: Content van Koppen in type 
2. Data: QUestions in type
3. Enable/Disable Questions en Reactions in type
4. Rating voor text-version-question


1. star-rating voor anonymous users
2. gebruik slug voor brief waarderen
3. multi site (NiceToHave)

1. Export csv van waarderingen
2. Export mailadressen voor 

1. style: brief in blok tonen
2. Iframe include mechanisme


1. Testcases voor improvetext


1. improvetext module in Git
2. Deploy improvetext naar citizenline



Andere Epics:
- Website voor citizeline
- Automated deployments
- Vagrant of docker box voor testing



Maak gebruik van iframe include.

Als alternatief ook een API bieden met:

css
javascript die zelf gebruikt kan worden
API calls voor ophalen / tonen van content, ratings en comments

                {% render_question_list for blog.post object_pk as comment_list %}
                {% for comment in comment_list %}
                <p>Posted by: {{ comment.user_name }} on {{ comment.submit_date }}</p>
                ...
                <p>Comment: {{ comment.comment }}</p>
                ...
                {% endfor %}
                
                
                
            {%
                def items(self):
        qs = django_comments.get_model().objects.filter(
            site__pk=self.site.pk,
            is_public=True,
            is_removed=False,
        )
        return qs.order_by('-submit_date')[:40]
 %}