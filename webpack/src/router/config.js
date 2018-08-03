
import Cs from '../cs/cs.vue'


export default{
	routes:[
		
		{path:'/cs_js', component:Cs},
		{path:'*', redirect:'/cs_js'}
	]
}
