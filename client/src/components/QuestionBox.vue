<template>
  <div class="card-body d-flex flex-column">
    <b-card title="What is Python?">
      <b-card-text>
        Python is a popular language commonly used in programming interviews.
        It is know for its pseudo code like syntax.
      </b-card-text>
      <b-button variant="success">Update</b-button>
      <b-button variant="danger">Delete</b-button>
    </b-card>
  </div>
</template>

<style scoped>
.card {
  text-align: left;
}
.btn {
  margin: 0 5px;
}

.card-text:hover {
  background: #eee;
  cursor: pointer;
}
</style>
