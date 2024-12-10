<script setup>
import VerticalNavGroup from '@layouts/components/VerticalNavGroup.vue';
import VerticalNavLink from '@layouts/components/VerticalNavLink.vue';
</script>

<template>
    <!-- 👉 Dashboards -->
    <VerticalNavGroup
        :item="{
            title: 'Dashboards',
            badgeContent: '5',
            badgeClass: 'bg-error',
            icon: 'bx-home-smile'
        }"
    >
        <VerticalNavLink
            :item="{
                title: 'Analytics',
                to: '/dashboard'
            }"
        />
        <VerticalNavLink
            :item="{
                title: 'CRM',
                to: '/dashboard/crm',
                badgeContent: 'Pro',
                badgeClass: 'bg-light-primary text-primary'
            }"
        />
        <VerticalNavLink
            :item="{
                title: 'ECommerce',
                to: '/dashboard/ecommerce',
                badgeContent: 'Pro',
                badgeClass: 'bg-light-primary text-primary'
            }"
        />
        <VerticalNavLink
            :item="{
                title: 'Academy',
                to: '/dashboard/academy',
                badgeContent: 'Pro',
                badgeClass: 'bg-light-primary text-primary'
            }"
        />
        <VerticalNavLink
            :item="{
                title: 'Logistics',
                target: '_blank',
                badgeContent: 'Pro',
                badgeClass: 'bg-light-primary text-primary'
            }"
        />
    </VerticalNavGroup>

    <!-- 👉 Front Pages -->
    <VerticalNavGroup
        :item="{
            title: 'Sentiments Data',
            badgeContent: '5',
            badgeClass: 'bg-error',
            icon: 'bx-file'
        }"
    >
        <VerticalNavLink
            :item="{
                title: 'Popular Instructors',
                to: '/sentiments-data/popular-instructors'
            }"
        />
        <VerticalNavLink
            :item="{
                title: 'Most Popular Modules',
                target: '_blank'
            }"
        />
        <VerticalNavLink
            :item="{
                title: 'Best Learning Modules',
                target: '_blank'
            }"
        />
        <VerticalNavLink
            :item="{
                title: 'Learning Modules Improvement',
                href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/front-pages/checkout',
                target: '_blank'
            }"
        />
    </VerticalNavGroup>

    <!-- 👉 Apps & Pages -->
    <!-- <VerticalNavSectionTitle
    :item="{
      heading: 'Apps & Pages',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Email',
      icon: 'bx-envelope',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/apps/email',
      target: '_blank',
      badgeContent: 'Pro',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Chat',
      icon: 'bx-chat',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/apps/chat',
      target: '_blank',
      badgeContent: 'Pro',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Calendar',
      icon: 'bx-calendar',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/apps/calendar',
      target: '_blank',
      badgeContent: 'Pro',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Kanban',
      icon: 'bx-grid',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/apps/kanban',
      target: '_blank',
      badgeContent: 'Pro',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Account Settings',
      icon: 'bx-user',
      to: '/account-settings',
    }"
  />

  <VerticalNavLink
    :item="{
      title: 'Login',
      icon: 'bx-log-in',
      to: '/login',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Register',
      icon: 'bx-user-plus',
      to: '/register',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Error',
      icon: 'bx-info-circle',
      to: '/no-existence',
    }"
  /> -->

    <!-- 👉 User Interface -->
    <!-- <VerticalNavSectionTitle
    :item="{
      heading: 'User Interface',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Typography',
      icon: 'bx-text',
      to: '/typography',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Icons',
      icon: 'bx-package',
      to: '/icons',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Cards',
      icon: 'bx-credit-card',
      to: '/cards',
    }"
  /> -->

    <!-- 👉 Forms & Tables -->
    <!-- <VerticalNavSectionTitle
    :item="{
      heading: 'Forms & Tables',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Form Layouts',
      icon: 'bx-layout',
      to: '/form-layouts',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Form Validation',
      icon: 'bx-check-circle',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/forms/form-validation',
      target: '_blank',
      badgeContent: 'Pro',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Form Wizard',
      icon: 'bx-align-middle',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/forms/form-wizard-numbered',
      target: '_blank',
      badgeContent: 'Pro',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Tables',
      icon: 'bx-table',
      to: '/tables',
    }"
  /> -->

    <!-- 👉 Others -->
    <!-- <VerticalNavSectionTitle
    :item="{
      heading: 'Others',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Access Control',
      icon: 'bx-command',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/demo-1/access-control',
      target: '_blank',
      badgeContent: 'Pro',
      badgeClass: 'bg-light-primary text-primary',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Documentation',
      icon: 'bx-file',
      href: 'https://demos.themeselection.com/sneat-vuetify-vuejs-admin-template/documentation/',
      target: '_blank',
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Raise Support',
      href: 'https://github.com/themeselection/sneat-vuetify-vuejs-admin-template-free/issues',
      icon: 'bx-phone',
      target: '_blank',
    }"
  /> -->
</template>
