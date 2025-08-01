custom_css = '''
<style>
    /* --- Textos de Instrução ("Arraste e solte" e "Limite") --- */

    /* Esconde completamente os elementos de texto originais para evitar conflitos. */
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] small {
        display: none;
    }

    /* Adiciona o novo texto de "Arraste e solte" usando o container pai.
       Isto garante que o texto flua naturalmente no layout. */
    [data-testid="stFileUploaderDropzoneInstructions"]::before {
        content: "Arraste e solte os arquivos aqui (200MB/arquivo)";
        display: block;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }

    /* --- Botão "Procurar Arquivos" --- */

    /* Esconde o texto original "Browse files" tornando a sua fonte de tamanho zero. */
    [data-testid="stFileUploaderDropzone"] button[data-testid="stBaseButton-secondary"] {
        font-size: 0;
    }

    /* Adiciona o novo texto em português e restaura um tamanho de fonte legível.
       Isto evita problemas de layout causados por 'position: absolute'. */
    [data-testid="stFileUploaderDropzone"] button[data-testid="stBaseButton-secondary"]::after {
        content: "Procurar Arquivos";
        font-size: 0.875rem; /* Ajuste o tamanho da fonte conforme necessário */
    }
</style>
'''