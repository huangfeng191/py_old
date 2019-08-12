
import BMap from '../views/bMap.vue'
import Chart from '../views/chart.vue'



export default{
	routes:[
		{path:'/bMap', component:BMap},
        {path:'/chart', component:Chart},
        {path:'*', redirect:'/chart'}
	]
}
