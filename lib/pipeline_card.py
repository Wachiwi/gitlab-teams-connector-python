from card import Card

class PipelineCard(Card):

    def __init__(self, payload):
        self.__parse(payload)

    def __generate_text(self):
        self.text = 'Pipeline '
        self.text += self.__status_phrase()
        self.text += 'for branch `{0}` '.format(self.branch)
        self.text += 'in [{0}]({1})'.format(self.project_name, self.project_url)

    def __status_phrase(self):
        print self.status
        if self.status == 'success':
            return 'succeeded '
        elif self.status == 'failed':
            return self.status +' '
        elif self.status == 'running':
            return self.status + ' '
        else:
            return 'is stuck '

    def __parse(self, payload):
        self.author = payload['user']['name']
        self.project_name = payload['project']['path_with_namespace']
        self.project_url  = payload['project']['web_url']

        self.branch = payload['object_attributes']['ref']
        self.status = payload['object_attributes']['status']

        self.__generate_text()

    def to_dict(self):
        return {
                'title': 'Pipeline event',
                'text': self.text
                }
