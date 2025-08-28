from django import forms

from .models import Quote, Source, Category


class QuoteForm(forms.ModelForm):
    category = forms.IntegerField()
    source = forms.CharField(max_length=100, label="Источник")

    class Meta:
        model = Quote
        fields = ['text', 'weight']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        category = self.cleaned_data['category']
        source_name = self.cleaned_data['source']

        source_obj, _ = Source.objects.get_or_create(
            name=source_name,
            category=category,
            user=self.user,
        )

        quote = Quote(
            text=self.cleaned_data['text'],
            source=source_obj,
            weight=self.cleaned_data['weight'],
            user=self.user,
        )

        if commit:
            quote.save()
        return quote

    def clean(self):
        cleaned = super().clean()
        category_id = self.data.get('category')
        if not category_id:
            raise forms.ValidationError("Выберите категорию")
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise forms.ValidationError("Неверная категория")
        cleaned['category'] = category

        source = cleaned.get('source')
        if not source:
            self.add_error('source', 'Укажите источник')
            return cleaned

        src = Source.objects.filter(name=source, category=category).first()
        if src and Quote.objects.filter(source=src).count() >= 3:
            self.add_error('source', 'У этого источника уже 3 цитаты — нельзя добавить ещё.')

    def clean_text(self):
        text = self.cleaned_data['text']
        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError('Такая цитата уже есть в базе')
        return text