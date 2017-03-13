from card import Card

class CommitCommentCard(Card):

    def __init__(self, payload):
        self.__parse(payload)

    def __generate_text(self):
        self.text = '{0} wrote a comment'.format(self.author)
        self.text += 'for commit `[{0}]({1})` '.format(self.commit, self.comment_url)
        self.text += 'in [{0}]({1}) <br/>'.format(self.project_name, self.project_url)
        self.text += '> {0}'.format(self.comment)

    def __parse(self, payload):
        self.author = payload['user']['name']
        self.project_name = payload['project']['path_with_namespace']
        self.project_url  = payload['project']['web_url']

        self.commit = payload['object_attributes']['commit_id']
        self.comment_url = payload['object_attributes']['url']
        self.comment = payload['object_attributes']['note']

        self.__generate_text()

    def to_dict(self):
        return {
                'title': 'Comment event',
                'text': self.text
                }
