import json

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from comments.models import Comment


# Create your views here.
@require_POST
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user != request.user:
        return HttpResponseForbidden()

    comment.delete()
    return JsonResponse({'success': 'True'})

@require_POST
def edit_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user != request.user:
        return HttpResponseForbidden()

    data = json.loads(request.body)
    comment.text = data.get('text', '')
    comment.save()
    return JsonResponse({'success': 'True'})