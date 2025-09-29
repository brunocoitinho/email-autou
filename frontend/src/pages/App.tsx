import { useState, useRef } from 'react';
import styles from "./styles.module.css";

// Define the structure of the API response
interface AnalysisResult {
  category: string;
  suggested_response: string;
}

function App() {
  const [emailText, setEmailText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setEmailText(''); // Clear text area when a file is selected
      setError('');
    }
  };

  const handleRemoveFile = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsLoading(true);
    setResult(null);
    setError('');

    let endpoint = '';
    let body: BodyInit | null = null;
    const headers: HeadersInit = {};

    if (file) {
      // Handle file upload
      endpoint = '/api/upload-file';
      const formData = new FormData();
      formData.append('file', file);
      body = formData;
    } else if (emailText.trim()) {
      // Handle text input
      endpoint = '/api/process-email';
      body = JSON.stringify({ email_text: emailText });
      headers['Content-Type'] = 'application/json';
    } else {
      setError('Por favor, insira um texto de e-mail ou envie um arquivo.');
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: headers,
        body: body,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ocorreu um erro na análise.');
      }

      const data: AnalysisResult = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Não foi possível conectar ao backend.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <h1 className={styles.header__title}>Analisador de E-mails com IA</h1>
        <p className={styles.header__description}>
          Cole o conteúdo de um e-mail abaixo ou envie um arquivo para classificá-lo e receber uma sugestão de resposta.
        </p>
      </header>

      <section id="form-section" className={styles.form__container}>
        <form id="email-form" onSubmit={handleSubmit}>
          <div className={styles.form__group}>
            <label htmlFor="email-text" className={styles.form__label}>Conteúdo do E-mail:</label>
            <textarea
              id="email-text"
              name="email-text"
              className={styles.form__textarea}
              placeholder="Cole o texto do e-mail aqui..."
              value={emailText}
              onChange={(e) => {
                setEmailText(e.target.value);
                setFile(null); // Clear file when text is typed
                if (fileInputRef.current) fileInputRef.current.value = '';
                setError('');
              }}
              required={!file} // Text is required if no file is present
            />
          </div>

          <div className={styles.form__group} style={{ textAlign: 'center', margin: '1rem 0' }}>
            <span className={styles.form__label}>OU</span>
          </div>
          
          <div className={styles.form__group} style={{display: 'flex', alignItems: 'center', gap: '10px', justifyContent: 'center', textAlign: 'center', margin: '1rem 0'}}>
            <label htmlFor="email-file" className={styles.form__file}>
              {file ? `Arquivo selecionado: ${file.name}` : 'Envie um arquivo (.txt ou .pdf)'}
            </label>
            <div className={styles.form__file__container}>
              <input
                type="file"
                id="email-file"
                name="email-file"
                style={{ display: 'none' }}
                accept=".txt, .pdf"
                onChange={handleFileChange}
                ref={fileInputRef}
              />
              {file && (
                <button type="button" onClick={handleRemoveFile} className={`${styles.form__button} ${styles.form__button__remove}`}>
                  X
                </button>
              )}
            </div>
          </div>

          <button type="submit" className={styles.form__button} disabled={isLoading}>
            {isLoading ? 'Analisando...' : 'Analisar E-mail'}
          </button>
        </form>
      </section>

      {error && (
        <div id="error-section" className={styles.error}>
          <p>{error}</p>
        </div>
      )}

      {isLoading && (
        <div id="loader" className={styles.loader}>
          <p>Analisando com a IA, por favor aguarde...</p>
          {/* You can add a spinner here */}
        </div>
      )}

      {result && (
        <section id="results-section" className={styles.results__container}>
          <h2 className={styles.results__title}>Resultado da Análise</h2>
          <div className={styles.results__item}>
            <strong>Categoria:</strong>
            <p id="result-category" className={result.category === 'Productive' ? styles.productive : styles.improductive}>
              {result.category}
            </p>
          </div>
          <div className={styles.results__item}>
            <strong>Resposta Sugerida:</strong>
            <p id="result-response">{result.suggested_response}</p>
          </div>
        </section>
      )}
    </main>
  );
}

export default App;