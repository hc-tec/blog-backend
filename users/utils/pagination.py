from rest_framework.pagination import PageNumberPagination


class SortedBlogPagination(PageNumberPagination):
    def get_paginated_response(self, data: []):
        data.sort(key=lambda x: x["create_time"], reverse=True)
        data.sort(key=lambda x:x["weight"], reverse=True)
        return super().get_paginated_response(data)
