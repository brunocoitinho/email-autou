import { useState, useRef } from 'react';
import styles from "./styles.module.css"

function App() {
  const [fileName, setFileName] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFileName(file.name);
    }
  };

  const handleRemoveFile = () => {
    setFileName('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
      <main className={styles.main}>
        <header className={styles.header}>
            <h1 className={styles.header__title}>Analisador de E-mails com IA</h1>
            <p className={styles.header__description}>Cole o conteúdo de um e-mail abaixo para classificá-lo como produtivo ou improdutivo e receber uma sugestão de resposta.</p>
        </header>

        
        <section id="form-section" className={styles.form__container}>
            <form id="email-form">
                <div className={styles.form__group}>
                    <label htmlFor="email-text" className={styles.form__label}>Conteúdo do E-mail:</label>
                    <textarea id="email-text" name="email-text" className={styles.form__textarea} placeholder="Cole o texto do e-mail aqui..." required></textarea>
                </div>
                
                <div className={styles.form__group} style={{display: 'flex', justifyContent: 'center'}}>
                  <div className={styles.form__file_container}>
                    <label htmlFor="email-file" className={styles.form__file}>{fileName ? `Arquivo: ${fileName}` : 'Ou envie um arquivo (.txt, .pdf):'}</label>
                    {fileName && <button type="button" onClick={handleRemoveFile} className={`${styles.form__button} ${styles.form__button__remove}`}>X</button>}
                  </div>
                    <input type="file" id="email-file" name="email-file" style={{display: 'none'}} accept=".txt,.pdf" onChange={handleFileChange} ref={fileInputRef} />
                </div>

                <button type="submit" className={styles.form__button}>Analisar E-mail</button>
            </form>
        </section>

        <section id="results-section" style={{display: 'none'}}>
            <h2>Resultado da Análise</h2>
            <div>
                <strong>Categoria:</strong>
                <p id="result-category">-</p>
            </div>
            <div>
                <strong>Resposta Sugerida:</strong>
                <p id="result-response">-</p>
            </div>
        </section>
        
        <div id="loader" style={{display: 'none'}}>
            <p>Analisando com a IA, por favor aguarde...</p>
        </div>

      </main>
  )
}

export default App
