
import BMap from '../views/bMap.vue'
import Chart from '../views/chart.vue'
import House from '../views/house/house.vue'



export default{
	routes:[
		{path:'/bMap', component:BMap},
        {path:'/chart', component:Chart},
        {path:'/house', component:House},
        {path:'*', redirect:'/house'}
	]
}
