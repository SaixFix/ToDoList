from django.db import transaction
from rest_framework import serializers

from core.models import User
from goals.models.board import Board, BoardParticipant


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices[1:]
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "is_deleted")

    def update(self, instance: Board, validated_data: dict) -> Board:
        # # ваш код для работы с участниками
        with transaction.atomic():
            #Фильтруем по текущей доске икслючая владельца и удаляем
            BoardParticipant.objects.filter(board=instance).exclude(user=self.context["request"].user).delete()
            BoardParticipant.objects.bulk_create([
                BoardParticipant(
                    user=participant["user"],
                    role=participant["role"],
                    board=instance
                )
                for participant in validated_data.get("participants", [])
            ])
            if title := validated_data.get("title"):
                instance.title = title
            instance.save(update_fields=("title",))
        return instance