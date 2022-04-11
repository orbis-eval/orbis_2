export enum enAnnotationStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  EDITED = 'edited',
  REPLACED = 'replaced',
  DELETED = 'deleted',
  NEW = 'new',
  PROVISORY = 'provisory'
}

export class Annotation {
  key: string;
  type: string;
  surface_form: string;
  start: number;
  end: number;
  scope: string;
  meta: {};
  status: enAnnotationStatus;
  index: number;
  hover = false;
  selected = false;

  constructor(obj?: any) {
    Object.assign(this, obj);
  }

  GetAnnotationForServerExchange(): any {
    return {
      key: this.key,
      type: this.type,
      surface_form: this.surface_form,
      start: this.start,
      end: this.end,
      scope: this.scope,
      meta: this.meta
    };
  }
}
