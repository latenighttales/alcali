import Vue from "vue";
import Router from "vue-router";
import store from "./store";
import Home from "./views/Home.vue";
import Login from "./views/Login";
import Jobs from "./views/Jobs";
import Keys from "./views/Keys";
import Minions from "./views/Minions";
import MinionDetail from "./views/MinionDetail";
import JobDetail from "./views/JobDetail";
import Events from "./views/Events";
import Run from "./views/Run";
import Settings from "./views/Settings";
import Conformity from "./views/Conformity";
import ConformityDetail from "./views/ConformityDetail";
import Users from "./views/Users";
import Schedules from "./views/Schedules";
import NotFound from "./components/NotFound";
import Search from "./views/Search";
import JobTemplates from "./views/JobTemplates";
import PersonalSettings from "./views/PersonalSettings";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/usersettings",
      name: "user_settings",
      component: PersonalSettings,
    },
    {
      path: "/minions",
      name: "minions",
      component: Minions,
    },
    {
      path: "/minions/:minion_id",
      name: "minion_detail",
      component: MinionDetail,
      props: true,
    },
    {
      path: "/jobs",
      name: "jobs",
      component: Jobs,
    },
    {
      path: "/jobs/:jid",
      name: "job_jid",
      component: Jobs,
      props: true,
    },
    {
      path: "/jobs/:jid/:minion_id",
      name: "job_detail",
      component: JobDetail,
      props: true,
    },
    {
      path: "/run",
      name: "run",
      component: Run,
    },
    {
      path: "/job_templates",
      name: "job_templates",
      component: JobTemplates,
    },
    {
      path: "/keys",
      name: "keys",
      component: Keys,
    },
    {
      path: "/events",
      name: "events",
      component: Events,
    },
    {
      path: "/conformity",
      name: "conformity",
      component: Conformity,
    },
    {
      path: "/conformity/:minion_id",
      name: "conformity_detail",
      component: ConformityDetail,
      props: true,
    },
    {
      path: "/schedules",
      name: "schedules",
      component: Schedules,
    },
    {
      path: "/users",
      name: "users",
      component: Users,
    },
    {
      path: "/settings",
      name: "settings",
      component: Settings,
    },
    {
      path: "/search",
      name: "search",
      component: Search,
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
      meta: {
        plainLayout: true,
      },
    },
    { path: "*", component: NotFound },
    /*
        {
          path: '/about',
          name: 'about',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/!* webpackChunkName: "about" *!/ './views/About.vue')
        },
    */
  ],
});

router.beforeEach((to, from, next) => {
  if (!store.getters.isLoggedIn && to.path !== "/login") {
    next("/login");
  } else if (to.path === "/login" && store.getters.isLoggedIn) {
    next("/");
  } else {
    next();
  }
});

export default router;
