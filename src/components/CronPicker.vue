<template>
  <div class="text-center">
    <v-menu
        v-model="menu"
        :close-on-content-click="false"
        :nudge-width="200"
        offset-x
    >
      <template v-slot:activator="{ on }">
        <v-text-field label="cron" v-on="on" v-model="cron"></v-text-field>
      </template>
      <v-card>
        <v-tabs
            v-model="tab"
            background-color="transparent"
        >
          <v-tab
              v-for="item in crondata"
              :key="item.name"
          >
            {{ item.name }}
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item
              v-for="item in crondata"
              :key="item.name"
          >
            <v-card flat>
              <v-card-text v-if="item.name !== 'Week'&&item.name !== 'Day'">
                <v-radio-group v-model="item.cronEvery" :mandatory="false">
                  <v-radio :label="item.every" value="1"></v-radio>
                  <v-radio value="2">
                    <template v-slot:label>
                      {{item.interval[0]}}
                      <v-text-field
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          v-model="item.incrementIncrement"
                      ></v-text-field>
                      {{item.interval[1]||""}}
                      <v-text-field
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          v-model="item.incrementStart"
                      ></v-text-field>
                      {{item.interval[2]||""}}
                    </template>
                  </v-radio>
                  <v-radio value="3">
                    <template v-slot:label>
                      {{item.specific}}
                      <v-select
                          v-model="item.specificSpecific"
                          :items="item.specificSpecificItems"
                          chips
                          multiple
                      ></v-select>
                    </template>
                  </v-radio>
                  <v-radio value="4">
                    <template v-slot:label>
                      {{item.cycle[0]}}
                      <v-text-field
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          v-model="item.rangeStart"
                      ></v-text-field>
                      {{item.cycle[1]||""}}
                      <v-text-field
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          v-model="item.rangeEnd"
                      ></v-text-field>
                      {{item.cycle[2]||""}}
                    </template>
                  </v-radio>
                </v-radio-group>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <v-divider></v-divider>
        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn text @click="menu = false">{{$t('components.CronPicker.Cancel')}}</v-btn>
          <v-btn color="primary" text @click="menu = false">{{$t('components.CronPicker.Save')}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
  export default {
    name: "CronPicker",
    methods: {
      range(size, startAt = 0) {
        return [...Array(size).keys()].map(i => i + startAt)
      },
    },
    computed: {
      cron() {
        return `${this.secondsText || "*"} ${this.minutesText || "*"} ${this.hoursText || "*"} ${this.daysText || "*"} ${this.monthsText || "*"} ${this.weeksText || "?"} ${this.yearsText || "*"}`
      },
      secondsText() {
        let seconds = ""
        let cronEvery = this.crondata.second.cronEvery
        console.log(cronEvery)
        switch (cronEvery.toString()) {
          case "1":
            seconds = "*"
            break
          case "2":
            seconds = this.crondata.second.incrementStart + "/" + this.crondata.second.incrementIncrement
            break
          case "3":
            this.crondata.second.specificSpecific.map(val => {
              seconds += val + ","
            })
            seconds = seconds.slice(0, -1)
            break
          case "4":
            seconds = this.crondata.second.rangeStart + "-" + this.crondata.second.rangeEnd
            break
        }
        return seconds
      },
      minutesText() {
        let minutes = ""
        let cronEvery = this.crondata.minute.cronEvery
        switch (cronEvery.toString()) {
          case "1":
            minutes = "*"
            break
          case "2":
            minutes = this.crondata.minute.incrementStart + "/" + this.crondata.minute.incrementIncrement
            break
          case "3":
            this.crondata.minute.specificSpecific.map(val => {
              minutes += val + ","
            })
            minutes = minutes.slice(0, -1)
            break
          case "4":
            minutes = this.crondata.minute.rangeStart + "-" + this.crondata.minute.rangeEnd
            break
        }
        return minutes
      },
      hoursText() {
        let hours = ""
        let cronEvery = this.crondata.hour.cronEvery
        switch (cronEvery.toString()) {
          case "1":
            hours = "*"
            break
          case "2":
            hours = this.crondata.hour.incrementStart + "/" + this.crondata.hour.incrementIncrement
            break
          case "3":
            this.crondata.hour.specificSpecific.map(val => {
              hours += val + ","
            })
            hours = hours.slice(0, -1)
            break
          case "4":
            hours = this.crondata.hour.rangeStart + "-" + this.crondata.hour.rangeEnd
            break
        }
        return hours
      },
      daysText() {
        let days = ""
        let cronEvery = this.crondata.day.cronEvery
        switch (cronEvery.toString()) {
          case "1":
            break
          case "2":
          case "4":
          case "11":
            days = "?"
            break
          case "3":
            days = this.crondata.day.incrementStart + "/" + this.crondata.day.incrementIncrement
            break
          case "5":
            this.crondata.day.specificSpecific.map(val => {
              days += val + ","
            })
            days = days.slice(0, -1)
            break
          case "6":
            days = "L"
            break
          case "7":
            days = "LW"
            break
          case "8":
            days = this.crondata.day.cronLastSpecificDomDay + "L"
            break
          case "9":
            days = "L-" + this.crondata.day.cronDaysBeforeEomMinus
            break
          case "10":
            days = this.crondata.day.cronDaysNearestWeekday + "W"
            break
        }
        return days
      },
      weeksText() {
        let weeks = ""
        let cronEvery = this.crondata.day.cronEvery
        switch (cronEvery.toString()) {
          case "1":
          case "3":
          case "5":
            weeks = "?"
            break
          case "2":
            weeks = this.crondata.week.incrementStart + "/" + this.crondata.week.incrementIncrement
            break
          case "4":
            this.crondata.week.specificSpecific.map(val => {
              weeks += val + ","
            })
            weeks = weeks.slice(0, -1)
            break
          case "6":
          case "7":
          case "8":
          case "9":
          case "10":
            weeks = "?"
            break
          case "11":
            weeks = this.crondata.week.cronNthDayDay + "#" + this.crondata.week.cronNthDayNth
            break
        }
        return weeks
      },
      monthsText() {
        let months = ""
        let cronEvery = this.crondata.month.cronEvery
        switch (cronEvery.toString()) {
          case "1":
            months = "*"
            break
          case "2":
            months = this.crondata.month.incrementStart + "/" + this.crondata.month.incrementIncrement
            break
          case "3":
            this.crondata.month.specificSpecific.map(val => {
              months += val + ","
            })
            months = months.slice(0, -1)
            break
          case "4":
            months = this.crondata.month.rangeStart + "-" + this.crondata.month.rangeEnd
            break
        }
        return months
      },
      yearsText() {
        let years = ""
        let cronEvery = this.crondata.year.cronEvery
        switch (cronEvery.toString()) {
          case "1":
            years = "*"
            break
          case "2":
            years = this.crondata.year.incrementStart + "/" + this.crondata.year.incrementIncrement
            break
          case "3":
            this.crondata.year.specificSpecific.map(val => {
              years += val + ","
            })
            years = years.slice(0, -1)
            break
          case "4":
            years = this.crondata.year.rangeStart + "-" + this.crondata.year.rangeEnd
            break
        }
        return years
      },
    },
    data() {
      return {
        menu: false,
        tabs: 3,
        tab: null,
        crondata: {
          second: {
            cronEvery: "",
            incrementStart: "3",
            incrementIncrement: "5",
            rangeStart: "",
            rangeEnd: "",
            specificSpecific: [],
            specificSpecificItems: this.range(60),
            name: "Seconds",
            every: "Every second",
            interval: ["Every", "second(s) starting at second"],
            specific: "Specific second (choose one or many)",
            cycle: ["Every second between second", "and second"],
          },
          minute: {
            cronEvery: "",
            incrementStart: "3",
            incrementIncrement: "5",
            rangeStart: "",
            rangeEnd: "",
            specificSpecific: [],
            specificSpecificItems: this.range(60),
            name: "Minutes",
            every: "Every minute",
            interval: ["Every", "minute(s) starting at minute"],
            specific: "Specific minute (choose one or many)",
            cycle: ["Every minute between minute", "and minute"],
          },
          hour: {
            cronEvery: "",
            incrementStart: "3",
            incrementIncrement: "5",
            rangeStart: "",
            rangeEnd: "",
            specificSpecific: [],
            specificSpecificItems: this.range(24),
            name: "Hours",
            every: "Every hour",
            interval: ["Every", "hour(s) starting at hour"],
            specific: "Specific hour (choose one or many)",
            cycle: ["Every hour between hour", "and hour"],
          },
          day: {
            cronEvery: "",
            incrementStart: "1",
            incrementIncrement: "1",
            rangeStart: "",
            rangeEnd: "",
            specificSpecific: [],
            cronLastSpecificDomDay: 1,
            cronDaysBeforeEomMinus: "",
            cronDaysNearestWeekday: "",
            name: "Day",
            every: "Every day",
            intervalWeek: ["Every", "day(s) starting on"],
            intervalDay: ["Every", "day(s) starting at the", "of the month"],
            specificWeek: "Specific day of week (choose one or many)",
            specificDay: "Specific day of month (choose one or many)",
            lastDay: "On the last day of the month",
            lastWeekday: "On the last weekday of the month",
            lastWeek: ["On the last", " of the month"],
            beforeEndMonth: ["day(s) before the end of the month"],
            nearestWeekday: ["Nearest weekday (Monday to Friday) to the", "of the month"],
            someWeekday: ["On the", "of the month"],
          },
          week: {
            cronEvery: "",
            incrementStart: "1",
            incrementIncrement: "1",
            specificSpecific: [],
            cronNthDayDay: 1,
            name: "Week",
            cronNthDayNth: "1",
            weekdayChoice: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
          },
          month: {
            cronEvery: "",
            incrementStart: "3",
            incrementIncrement: "5",
            rangeStart: "",
            rangeEnd: "",
            specificSpecific: [],
            specificSpecificItems: this.range(12),
            name: "Month",
            every: "Every month",
            interval: ["Every", "month(s) starting in"],
            specific: "Specific month (choose one or many)",
            cycle: ["Every month between", "and"],
          },
          year: {
            cronEvery: "",
            incrementStart: "2019",
            incrementIncrement: "1",
            rangeStart: "",
            rangeEnd: "",
            specificSpecific: [],
            specificSpecificItems: this.range(99, 2020),
            name: "Year",
            every: "Any year",
            interval: ["Every", "year(s) starting in"],
            specific: "Specific year (choose one or many)",
            cycle: ["Every year between", "and"],
          },
        },
        output: {
          second: "",
          minute: "",
          hour: "",
          day: "",
          month: "",
          Week: "",
          year: "",
        },
      }
    },
  }
</script>

<style scoped>

</style>