<template>
  <div class="search-results">
    <h2>Find Podcast</h2>
    <div class="search">
      <input v-model="searchTerm" @keyup.enter="searchForPodcast" />
      <button class="button" @click="searchForPodcast">Find Podcast</button>
    </div>
    <ul v-for="(searchResult, index) in searchResults" v-bind:key="index">
      <li
        @click="sendFeedtoApp(searchResult.feedUrl, searchResult.collectionName, searchResult.collectionId)"
      >
        {{searchResult.collectionName}}
        <button
          class="button"
          @click="subscribe(searchResult.feedUrl, searchResult.collectionName, searchResult.collectionId)"
        >{ buttonText }</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
import { searchBus } from "../main";

export default {
  name: "SearchResults",
  data() {
    return {
      searchTerm: "",
      searchResults: [],
      subscribing: false,
      subscriptions: [],
      disable_subscribe: false,
      show_podcast_API_id: [],
      buttonText: "",
      podcast_id: ""
    };
  },
  methods: {
    //searchForPodcast adds the searchTerm from the user to make a call to the itunes api. The data from this response is capped at 50 responses. This can be changed by setting the parameter in the itunes url though.
    searchForPodcast() {
      axios
        .get(
          "https://itunes.apple.com/search?term=" +
            this.searchTerm +
            "&country=US&media=podcast"
        )
        .then(data => {
          this.searchResults = data.data.results;
        });
    },
    subscribe(url, name, podcast_id) {
      this.subscribing = true;
      this.sendFeedtoApp(url, name, podcast_id);
    },
    sendFeedtoApp(url, name, podcast_id) {
      let isSubscribing = this.subscribing;
      searchBus.$emit("feedFromSearch", url, name, podcast_id, isSubscribing);
      this.subscribing = false;
    }
  },
  created() {}
};
</script>

<style>
</style>