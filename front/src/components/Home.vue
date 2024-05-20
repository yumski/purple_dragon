<template>
  <div id="home">
    <main>
      <section class="input-section">
        <h4>Upload a file...</h4>
        <FileUpload name="file" mode="basic" url="http://localhost:5000/api/upload"
          @before-upload="onBeforeUpload($event)" @upload="onUploadComplete($event)" @error="onUploadError($event)"
          accept="image/*" :auto="true" />
        <h4><object data="" type=""></object>or enter some ingredients...</h4>
        <Textarea v-model="ingredientsInput" placeholder="mustard, cheese, dough, sauce..." variant="filled" rows="5"
          cols="30" />
        <Button label="Submit" @click="handleSubmit" />
      </section>
      <Divider class="divider" type="dotted" />
      <ProgressSpinner v-if="loading" strokeWidth="6" aria-label="Loading" />
      <section>
        <CustomComponent v-for="(request, index) in requests" :key="index" :image="request.image" :tags="request.tags"
          :cards="request.recipes" />
      </section>
    </main>
  </div>
</template>

<script>
import Image from 'primevue/image';
import Button from 'primevue/button';
import Divider from 'primevue/divider';
import Textarea from 'primevue/textarea';
import FileUpload from 'primevue/fileupload';
import ProgressSpinner from 'primevue/progressspinner';

import CardGrid from './CardGrid.vue';
import CustomGrid from './CustomGrid.vue';
import CustomComponent from './CustomComponent.vue';

export default {
  name: 'Home',
  components: {
    CardGrid,
    CustomGrid,
    CustomComponent,
    Image,
    Button,
    Divider,
    Textarea,
    FileUpload,
    ProgressSpinner
  },
  data() {
    return {
      ingredientsInput: '',
      cards: [],
      requests: [],
      loading: false,
      error: false,
      userEmail: ''
    }
  },
  created() {
    const authHeaders = JSON.parse(localStorage.getItem('authHeaders'));
    if (authHeaders) {
      this.userEmail = authHeaders.username;
    } else {
      this.$router.push('/login');
    }
  },
  methods: {
    async handleSubmit() {
      if (this.ingredientsInput) {
        this.loading = true;
        const ingredientList = this.ingredientsInput.split(",").map((e) => e.trim());
        let body = {
          ingredients: ingredientList,
        };

        // POST ingredients to server to get a recipe back
        let response = await this.getRecipes("http://localhost:5000/api/recipes", body);
        if (response) {
          const recipes = response.map((recipe) => {
            recipe.tags = ingredientList;
            return recipe; // Don't forget to return the modified recipe object
          });
          await this.addRecipesToList(recipes, null);
        }
        this.ingredientsInput = '';
      }
    },
    async getRecipes(url, body) {
      // send async request to backend
      let serverResponse = null;
      try {
        const response = await fetch(url, {
          method: "POST",
          body: JSON.stringify(body),
          headers: {
            "Content-Type": "application/json",
          },
          credentials: 'include'
        });
        // get response from backend in the form of a json
        serverResponse = await response.json();
      } catch (error) {
        console.log("Error:", error);
        this.error = true;
      }
      return serverResponse;
    },
    async onBeforeUpload(event) {
      this.loading = true;
      //maybe retry with the below?
      https://stackoverflow.com/questions/57778172/input-form-provides-file-how-to-i-upload-it-to-azure-blob-storage-using-vue
      return null;
    },
    async onUploadComplete(event) {
      if (event.xhr.response) {
        const recipes = JSON.parse(event.xhr.response);
        await this.addRecipesToList(recipes, event.files[0].objectURL);
        console.log('Files:', event.files);
      }
      else {
        //insert gordo
        this.loading = false;
        this.error = true;
      }
    },
    async onUploadError(event) {
      if (event.xhr.response) {
        const error = JSON.parse(event.xhr.response);
        console.log("File Upload Error! => ", error);
      }
      this.loading = false;
      this.error = true;
    },
    async addRecipesToList(recipes, image) {
      const ingredients = recipes.pop();
      const request = {
        image: image,
        tags: ingredients.ingredients,
        recipes: recipes
      }
      this.requests.unshift(request);
      this.loading = false;
    }
  }
}
</script>

<style>
#home header {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--primary-color);
  padding: 1rem;
  color: var(--text-color);
}

.dashboard-button-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
  gap: 5rem;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  padding: 1rem;
}

.input-section {
  width: 50vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 1rem;
}

textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 0.5rem;
  background-color: var(--background-light-color);
}

.divider {
  color: var(--accent-color);
}

.p-progress-spinner-circle {
  width: 70px;
  height: 70px;
  stroke: var(--accent-color) !important;
}

.card-grid-section {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 80vw;
  padding-top: 2rem;
}
</style>
