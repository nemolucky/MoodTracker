from django.db import migrations, models


def populate_slugs(apps, schema_editor):
    Mood = apps.get_model("moods", "Mood")
    for mood in Mood.objects.using(schema_editor.connection.alias).all():
        mood.slug = f"mood-{mood.pk}"
        mood.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [("moods", "0001_initial")]
    operations = [
        migrations.AddField("mood", "slug", models.SlugField(null=True)),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
