from card import Card

class PushCard(Card):

    def __init__(self, payload):
        self.__parse(payload)

    def __generate_text(self):
        self.text = '{0} pushed '.format(self.author)
        self.text += self.__commit_phrase()
        self.text += '([{0}](1)) '.format(self.latest_commit_id, self.latest_commit_url)
        self.text += 'to branch {0} '.format(self.branch)
        self.text += 'in [{0}]({1})'.format(self.project_name, self.project_url)

    def __commit_phrase(self):
        if self.commits_count > 1:
            return '{0} commits '.format(self.commits_count)
        else:
            return 'a commit '

    def __parse(self, payload):
        self.author = payload['user_name']
        self.project_name = payload['project']['path_with_namespace']
        self.project_url  = payload['project']['web_url']
        self.branch = payload['ref'][11:]
        self.commits_count = payload['total_commits_count']
        self.latest_commit_id = payload['after']
        self.latest_commit_url = payload['commits'][0]['url']

        self.__generate_text()

    def to_dict(self):
        return {
                'title': 'Push Event',
                'text': self.text
                }
