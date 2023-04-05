from django.contrib import admin

from goals.models.goal import Goal
from goals.models.goal_category import GoalCategory
from goals.models.goal_comment import GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ("text", "goal", "user", "created", "updated")
    search_fields = ("text", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
