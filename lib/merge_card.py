from card import Card

class MergeCard(Card):

    def __init__(self, payload):
        self.__parse(payload)

    def __generate_text(self):
        self.text = '{0} '.format(self.author)
        self.text += self.__action_phrase()
        self.text += 'Merge Request in [{0}]({1}):<br/>'.format(self.project_name, self.project_url)
        self.text += '*{0}*'.format(self.mr_title)


    def __action_phrase(self):
        if self.action == 'update':
            return 'updated '
        elif self.action == 'create':
            return 'created '
        elif self.action == 'close':
            return 'closed '
        elif self.action == 'merge':
            return 'merged '
        elif self.action == 'reopen':
            return 'repoened '
        else:
            return 'modified '

    def __parse(self, payload):
        self.author = payload['user']['name']
        self.project_name = payload['project']['path_with_namespace']
        self.project_url  = payload['project']['web_url']

        self.action = payload['object_attributes']['action']
        self.mr_title = payload['object_attributes']['title']
        self.mr_url = payload['object_attributes']['url']

        self.__generate_text()

    def to_dict(self):
        return {
                'title': 'Merge Request event',
                'text': self.text,
                'potentialAction': [{
                    '@context': 'https://schema.org',
                    '@type': 'ViewAction',
                    'name': 'View Merge Request',
                    'target': [self.mr_url]
                    }]
                }
