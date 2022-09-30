
export interface IResponse<T> {
    status_code: number,
    message: string,
    content: T
}
