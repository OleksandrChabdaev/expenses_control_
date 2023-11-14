from django.db import migrations


def add_managers_group_permissions(apps, schema_editor):
    """
    Add permissions for "Managers" group.
    "Managers" have next permissions:
    - User - Can add/change/delete/view permission
    """
    group = apps.get_model("auth", "Group")
    permission = apps.get_model("auth", "Permission")
    db_alias = schema_editor.connection.alias
    permissions_code_names = [
        "add_user",
        "change_user",
        "delete_user",
        "view_user",
    ]
    permissions = permission.objects.using(db_alias).filter(
        codename__in=permissions_code_names
    )
    managers_group, created = group.objects.get_or_create(name="Managers")
    managers_group.permissions.set(permissions)


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_add_permissions_groups"),
    ]
    operations = [
        migrations.RunPython(add_managers_group_permissions),
    ]
