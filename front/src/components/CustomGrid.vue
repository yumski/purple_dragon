<template>
    <div class="p-grid">
        <div class="p-col-12 p-md-4">
            <Image src="/static/idiot-sandwich.jpg" alt="You Donkey!" />
        </div>
        <div class=" p-col-12 p-md-8">
            <div class="p-grid">
                <div class="p-col-12 p-md-6" v-for="(card, index) in cards" :key="index">
                    <Card>
                        <template #title>{{ card.title }}</template>
                        <template v-if="card.tags" #subtitle>{{ card.tags }}</template>
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
    </div>
</template>

<script>
import Card from 'primevue/card';
import Chip from 'primevue/chips';
import Divider from 'primevue/divider';
import Rating from 'primevue/rating';
import Image from 'primevue/image';

export default {
    name: 'CustomGrid',
    components: {
        Card,
        Chip,
        Divider,
        Rating,
        Image
    },
    props: {
        requests:
        {
            type: Array,
            required: true
        },
        image: {
            type: String,
            required: false
        },
        cards: {
            type: Array,
            required: true
        }
    }
};
</script>

<style scoped>
.image {
    width: 100%;
    height: auto;
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