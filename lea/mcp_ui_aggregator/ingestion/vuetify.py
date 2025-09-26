"""Vuetify (Vue.js) component ingestion module."""

from typing import List, Dict, Any
from .base import BaseIngestionModule


class VuetifyIngestionModule(BaseIngestionModule):
    """Vuetify Vue.js component ingestion."""
    
    def get_namespace(self) -> str:
        return "vuetify"
    
    def get_framework(self) -> str:
        return "vue"
    
    def get_base_url(self) -> str:
        return "https://vuetifyjs.com"
    
    def get_components(self) -> List[Dict[str, Any]]:
        """Vuetify Vue.js components."""
        return [
            {
                "name": "VBtn",
                "title": "Vuetify Button",
                "description": "The v-btn component replaces the standard html button with a material design theme and a multitude of options.",
                "component_type": "button",
                "category": "components",
                "framework": "vue",
                "tags": ["button", "vuetify", "vue", "material"],
                "documentation_url": f"{self.get_base_url()}/components/buttons/",
                "import_statement": '''import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

createApp().use(vuetify).mount('#app')''',
                "basic_usage": '<v-btn>Button</v-btn>',
                "variants": {
                    "primary": '<v-btn color="primary">Primary</v-btn>',
                    "secondary": '<v-btn color="secondary">Secondary</v-btn>',
                    "success": '<v-btn color="success">Success</v-btn>',
                    "error": '<v-btn color="error">Error</v-btn>',
                    "warning": '<v-btn color="warning">Warning</v-btn>',
                    "info": '<v-btn color="info">Info</v-btn>',
                    "outlined": '<v-btn variant="outlined">Outlined</v-btn>',
                    "text": '<v-btn variant="text">Text</v-btn>',
                    "fab": '<v-btn icon="mdi-heart" size="large"></v-btn>',
                    "loading": '<v-btn loading>Loading</v-btn>',
                    "disabled": '<v-btn disabled>Disabled</v-btn>',
                    "rounded": '<v-btn rounded>Rounded</v-btn>',
                    "block": '<v-btn block>Block</v-btn>'
                },
                "examples": [
                    {
                        "title": "Button with Icon",
                        "description": "Buttons can contain icons",
                        "code": '''<template>
  <v-btn prepend-icon="mdi-heart">
    Like
  </v-btn>
  <v-btn append-icon="mdi-arrow-right">
    Next
  </v-btn>
</template>'''
                    },
                    {
                        "title": "Button Group",
                        "description": "Group related buttons together",
                        "code": '''<template>
  <v-btn-group>
    <v-btn>Left</v-btn>
    <v-btn>Center</v-btn>
    <v-btn>Right</v-btn>
  </v-btn-group>
</template>'''
                    }
                ]
            },
            {
                "name": "VCard",
                "title": "Vuetify Card",
                "description": "The v-card component is a versatile component that can be used for anything from a panel to a static image.",
                "component_type": "display",
                "category": "components",
                "framework": "vue",
                "tags": ["card", "vuetify", "vue", "container"],
                "documentation_url": f"{self.get_base_url()}/components/cards/",
                "import_statement": '''import { VCard, VCardTitle, VCardText, VCardActions } from 'vuetify/components'

export default {
  components: {
    VCard,
    VCardTitle,
    VCardText,
    VCardActions
  }
}''',
                "basic_usage": '''<v-card>
  <v-card-title>Card Title</v-card-title>
  <v-card-text>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
  </v-card-text>
  <v-card-actions>
    <v-btn>Action</v-btn>
  </v-card-actions>
</v-card>''',
                "examples": [
                    {
                        "title": "Media Card",
                        "description": "Card with image and actions",
                        "code": '''<template>
  <v-card max-width="400">
    <v-img src="https://example.com/image.jpg" height="200"></v-img>
    <v-card-title>Card Title</v-card-title>
    <v-card-subtitle>Card Subtitle</v-card-subtitle>
    <v-card-text>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary">Learn More</v-btn>
      <v-spacer></v-spacer>
      <v-btn icon="mdi-heart" @click="liked = !liked" :color="liked ? 'red' : ''"></v-btn>
      <v-btn icon="mdi-share"></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      liked: false
    }
  }
}
</script>'''
                    }
                ]
            },
            {
                "name": "VDialog",
                "title": "Vuetify Dialog",
                "description": "The v-dialog component inform users about a task and can contain critical information, require decisions, or involve multiple tasks.",
                "component_type": "overlay",
                "category": "components",
                "framework": "vue",
                "tags": ["dialog", "modal", "vuetify", "vue"],
                "documentation_url": f"{self.get_base_url()}/components/dialogs/",
                "import_statement": '''import { VDialog } from 'vuetify/components'

export default {
  components: {
    VDialog
  }
}''',
                "basic_usage": '''<template>
  <div>
    <v-btn @click="dialog = true">Open Dialog</v-btn>
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>Dialog Title</v-card-title>
        <v-card-text>Dialog content goes here.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="dialog = false">Close</v-btn>
          <v-btn color="primary" @click="dialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: false
    }
  }
}
</script>'''
            },
            {
                "name": "VTextField",
                "title": "Vuetify Text Field",
                "description": "Text fields components are used for collecting user provided information.",
                "component_type": "input",
                "category": "forms",
                "framework": "vue",
                "tags": ["input", "textfield", "vuetify", "vue", "form"],
                "documentation_url": f"{self.get_base_url()}/components/text-fields/",
                "import_statement": '''import { VTextField } from 'vuetify/components'

export default {
  components: {
    VTextField
  }
}''',
                "basic_usage": '<v-text-field label="Label" v-model="value"></v-text-field>',
                "variants": {
                    "outlined": '<v-text-field variant="outlined" label="Outlined"></v-text-field>',
                    "filled": '<v-text-field variant="filled" label="Filled"></v-text-field>',
                    "underlined": '<v-text-field variant="underlined" label="Underlined"></v-text-field>',
                    "solo": '<v-text-field variant="solo" label="Solo"></v-text-field>',
                    "password": '<v-text-field type="password" label="Password"></v-text-field>',
                    "disabled": '<v-text-field disabled label="Disabled"></v-text-field>',
                    "readonly": '<v-text-field readonly label="Readonly" value="Read only text"></v-text-field>',
                    "with-icon": '<v-text-field prepend-icon="mdi-email" label="Email"></v-text-field>'
                },
                "examples": [
                    {
                        "title": "Form with Validation",
                        "description": "Text field with validation rules",
                        "code": '''<template>
  <v-form ref="form" v-model="valid">
    <v-text-field
      v-model="email"
      :rules="emailRules"
      label="E-mail"
      required
    ></v-text-field>
    <v-text-field
      v-model="password"
      :rules="passwordRules"
      label="Password"
      type="password"
      required
    ></v-text-field>
    <v-btn :disabled="!valid" color="success" @click="submit">
      Submit
    </v-btn>
  </v-form>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\\..+/.test(v) || 'E-mail must be valid',
      ],
      password: '',
      passwordRules: [
        v => !!v || 'Password is required',
        v => v.length >= 8 || 'Password must be at least 8 characters',
      ],
    }
  },
  methods: {
    submit() {
      console.log('Form submitted!')
    }
  }
}
</script>'''
                    }
                ]
            },
            {
                "name": "VAppBar",
                "title": "Vuetify App Bar",
                "description": "The v-app-bar component is pivotal to any graphical user interface (GUI), as it generally is the primary source of site navigation.",
                "component_type": "navigation",
                "category": "components",
                "framework": "vue",
                "tags": ["appbar", "navigation", "vuetify", "vue"],
                "documentation_url": f"{self.get_base_url()}/components/app-bars/",
                "import_statement": '''import { VAppBar, VToolbarTitle, VBtn } from 'vuetify/components'

export default {
  components: {
    VAppBar,
    VToolbarTitle,
    VBtn
  }
}''',
                "basic_usage": '''<v-app-bar>
  <v-toolbar-title>My Application</v-toolbar-title>
  <v-spacer></v-spacer>
  <v-btn icon="mdi-menu"></v-btn>
</v-app-bar>''',
                "examples": [
                    {
                        "title": "App Bar with Navigation",
                        "description": "App bar with navigation drawer toggle",
                        "code": '''<template>
  <v-app-bar app>
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    <v-toolbar-title>My App</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon="mdi-magnify"></v-btn>
    <v-btn icon="mdi-heart"></v-btn>
    <v-btn icon="mdi-dots-vertical"></v-btn>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {
      drawer: false
    }
  }
}
</script>'''
                    }
                ]
            },
            {
                "name": "VSnackbar",
                "title": "Vuetify Snackbar",
                "description": "The v-snackbar component is used to display a quick message to a user.",
                "component_type": "feedback",
                "category": "components",
                "framework": "vue",
                "tags": ["snackbar", "notification", "vuetify", "vue"],
                "documentation_url": f"{self.get_base_url()}/components/snackbars/",
                "import_statement": '''import { VSnackbar } from 'vuetify/components'

export default {
  components: {
    VSnackbar
  }
}''',
                "basic_usage": '''<template>
  <div>
    <v-btn @click="snackbar = true">Open Snackbar</v-btn>
    <v-snackbar v-model="snackbar">
      Hello, I'm a snackbar
      <template v-slot:actions>
        <v-btn color="pink" variant="text" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      snackbar: false
    }
  }
}
</script>'''
            }
        ]