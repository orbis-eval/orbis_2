
export class DocumentService {

    static async getCorpora() {
        const response = await fetch(`${import.meta.env.DEV ? 'http://localhost:63010/' : '/'}getCorpora`);
        return await response.json();
    }

    static async getDocuments(corpus: string) {
        const response = await fetch(`${import.meta.env.DEV ? 'http://localhost:63010/' : '/'}getDocumentsOfCorpus?corpus_name=${corpus}`);
        return await response.json();
    }
}
