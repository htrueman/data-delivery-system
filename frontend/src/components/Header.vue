<template lang="jade">
  .header.row
    .logo.col-md-10
      router-link(to="/")
         img(src="@/assets/img/dds_logo.png")
    .col-md-2
      // if not authed
      router-link(to="/", class="btn btn-primary sign-in-btn") Sign In
      // else
      router-link(to="/", class="btn btn-primary sign-in-btn") Sign Out
    //
      <div class="header row">
          <div class="logo col-md-10">
              <a href="{% url 'local_spider_manager:list' %}"><img src="{% static 'img/dds_logo.png' %}"></a>
          </div>
          <div class="col-md-2">
              {% if not user.is_authenticated %}
                  <a href="{% url 'core:login' %}" class="btn btn-primary sign-in-btn">Sign In</a>
              {% else %}
                  <a href="{% url 'core:logout' %}" class="btn btn-primary sign-out-btn">Sign Out</a>
              {% endif %}
          </div>
      </div>
</template>

<script>
  export default {
    name: 'Header'
  }
</script>

<style scoped>

</style>
