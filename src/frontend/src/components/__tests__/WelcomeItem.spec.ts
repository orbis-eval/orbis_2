import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import WelcomeItem from '../WelcomeItem.vue'

describe('WelcomeItem', () => {
  it ('renders',  () => {
    const wrapper = mount(WelcomeItem, {
      slots: {
        heading: 'Test Text',
        default: 'Lorem ipsum'
      }
    });
    expect(wrapper.find('h3').text()).toContain('Test Text');
    expect(wrapper.find('.details').text()).toContain('Lorem ipsum');
  });
});
