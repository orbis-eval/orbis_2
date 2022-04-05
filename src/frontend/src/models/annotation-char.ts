import {Annotation} from './annotation';
import {AnnotationType} from './annotation-type';

export class AnnotationCharObject {
  char: string;
  index: number;
  annotations: Annotation[] = [];
  type?: AnnotationType;

  constructor(obj?: any) {
    Object.assign(this, obj);
  }
}
