from card import Card
from mr_comment_card import MergeRequestCommentCard
from commit_comment_card import CommitCommentCard
from issue_comment_card import IssueCommentCard


class CommentCard(Card):

    @classmethod
    def get(cls, payload):
        comment_type = payload['object_attributes']['noteable_type']
        card = None
        if comment_type == 'Commit':
            card = CommitCommentCard(payload)
        elif comment_type == 'MergeRequest':
            card = MergeRequestCommentCard(payload)
        elif comment_type == 'Issue':
            card = IssueCommentCard(payload)
        print card
        print comment_type
        return card

