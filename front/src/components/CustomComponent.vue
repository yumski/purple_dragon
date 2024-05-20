<template>
    <div class="custom-component">
        <!-- Left Content Section -->
        <div class="left-content">
            <Image v-if="image" :src="image" width="300"></Image>
            <p>{{ tags }}</p>
        </div>

        <!-- Right Cards Section -->
        <div class="right-content">
            <div v-for="(card, index) in cards" :key="index" class="card">
                <!-- Card content -->
                <Card>
                    <template #title>{{ card.title }}</template>
                    <template #content>
                        <h3>Ingredients</h3>
                        <ul>
                            <li v-for="(ingredient, index) in card.ingredients" :key="index">{{ ingredient }}</li>
                        </ul>
                        <Divider layout="vertical" />
                        <h3>Directions</h3>
                        <ol>
                            <li v-for="(step, index) in card.directions" :key="index">{{ step }}</li>
                        </ol>
                    </template>
                    <template #footer>
                        <div class="flex gap-3 mt-1">
                            <Rating :cancel="false" />
                        </div>
                    </template>
                </Card>
            </div>
        </div>
    </div>
</template>
<script>
import Card from 'primevue/card';
import Chip from 'primevue/chips';
import Divider from 'primevue/divider';
import Rating from 'primevue/rating';
import Image from 'primevue/image';

export default {
    name: 'CustomComponent',
    components: {
        Card,
        Chip,
        Divider,
        Rating,
        Image
    },
    props: {
        image: {
            type: String
        },
        tags: {
            type: Array
        },
        cards: {
            type: Array,
            required: true
        }
    }
};
</script>
<style>
.custom-component {
    display: flex;
    gap: 1rem;
}

.left-content {
    width: 300px;
}

.right-content {
    width: 70%;
}

.card-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2.5rem;
    width: 100%;
}

.p-card {
    padding: 1rem;
    width: 100%;
    background-color: var(--background-light-color);
    color: var(--text-dark-color);
    border: 5px solid var(--accent-color);
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.p-card-title {
    /* background-color: var(--accent-color); */
    margin-bottom: 0;
}

.p-card-content {
    padding-top: 0;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
}

.p-divider {
    color: black;
}

.p-card-footer {
    /* background-color: white; */
    /* border: 4px solid red; */
}
</style>