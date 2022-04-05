export class AnnotationType {
  index: string;
  key: string;
  caption: string;

  constructor(obj?: any) {
    Object.assign(this, obj);
  }
}
