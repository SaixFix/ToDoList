from rest_framework import permissions

from goals.models.board import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        _filters: dict = {'user': request.user.id, 'board': obj}

        if request.method not in permissions.SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exclude()


class GoalCategoryPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        _filters: dict = {'user_id': request.user.id, 'board_id': obj.board_id}

        if request.method not in permissions.SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**_filters).exclude()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        _filters: dict = {'user_id': request.user.id, 'board_id': obj.category.board_id}

        if request.method not in permissions.SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**_filters).exclude()


class GoalCommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.user_id == request.user.id
