.PHONY: ci clean-pyc docs-serve tests

clean-pyc:
	find . -name '*.pyc' -type f -exec rm -f {} +
	find . -name '*.pyo' -type f -exec rm -f {} +
	find . -name '__pycache__' -type d -exec rm -rf {} +
	find . -name '.pytest_cache' -type d -exec rm -rf {} +

ci:
	docker-compose exec -u alcali web alcali migrate \
	&& docker-compose exec -u alcali web alcali shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').count() or User.objects.create_superuser('admin', 'admin@example.com', 'password')"

docs-serve:
	echo http://127.0.0.1:8060 \
	&& mkdocs serve -f docs/mkdocs.yml -a 127.0.0.1:8060

tests:
	@docker-compose exec -u alcali web pytest
