<template>
    <div>
        <h1>Tour Cost Calculator</h1>
        <label>
            Number of people:
            <input type="number" v-model.number="numPeople" min="1" />
        </label>

        <div v-if="tourData">
            <h2>Base cost: {{ tourData.base_cost }} € (per person)</h2>
            <div v-for="day in tourData.days" :key="day.id" class="tour-day">
                <h3>{{ day.id.toUpperCase() }}</h3>
                <p>{{ day.description }}</p>

                <div v-if="day.excursions && day.excursions.length">
                    <strong>Excursions:</strong>
                    <div v-for="exc in day.excursions" :key="exc.id">
                        <label v-if="exc.included">
                            <input type="checkbox" checked disabled />
                            {{ exc.name }} (Included)
                        </label>
                        <label v-else>
                            <input type="checkbox" :value="true" v-model="selectedExcursions[day.id].exc[exc.id]" />
                            {{ exc.name }} ({{ exc.cost_eur }} €)
                        </label>
                    </div>
                </div>

                <div v-if="day.food && day.food.length">
                    <strong>Food:</strong>
                    <div v-for="food in day.food" :key="food.name">
                        <label>
                            <input type="checkbox" :value="food.name" v-model="selectedFood[day.id]" />
                            {{ food.name }} ({{ food.cost_eur }} €)
                        </label>
                    </div>
                </div>
                <hr />
            </div>
        </div>

        <button @click="calculate">Calculate</button>

        <div v-if="total !== null">
            <h2>Total Cost: {{ total }} €</h2>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            tourData: null,
            selectedExcursions: [],
            selectedFood: {},
            numPeople: 1,
            total: null,
        };
    },
    created() {
        axios.get("http://localhost:5051/options").then((res) => {
            this.tourData = res.data;
            // Initialize selection objects for each day
            for (const day of res.data.days) {
                this.selectedExcursions[day.id] = {exc:{}};
                this.selectedFood[day.id] = [];
            }
        });
    },
    methods: {
        calculate() {
            // Prepare selected data for backend
            const selected = {
                excursions: {},
                food: {},
            };
            for (const day of this.tourData.days) {
                // Only send non-empty arrays
                if(this.selectedExcursions[day.id]&&this.selectedExcursions[day.id].exc&&Object.entries(this.selectedExcursions[day.id].exc).length){
                    selected.excursions[day.id] = [];
                    for(const [ind, exc] of Object.entries(this.selectedExcursions[day.id].exc)){
                        selected.excursions[day.id].push(ind);
                    }
                }
                selected.food[day.id] = this.selectedFood[day.id] || [];
            }
            axios
                .post("http://localhost:5051/calculate", {
                    num_people: this.numPeople,
                    selected,
                })
                .then((res) => {
                    this.total = res.data.total_cost_eur;
                });
        },
    },
};
</script>

<style>
.tour-day {
    margin-bottom: 2em;
}
</style>