import nef
import ca.nengo
import numeric
import spa.view
import spa.module

class Thalamus(spa.module.Module):
    def __init__(self,bg,**params):
        spa.module.Module.__init__(self,**params)
        self.bg=bg


    def create(self,rule_neurons=40,rule_threshold=0.2,bg_output_weight=-3,
               pstc_output=0.015,mutual_inhibit=1,pstc_inhibit=0.008,
               pstc_to_gate=0.002,pstc_gate=0.008,N_per_D=30,
               pstc_route_input=0.002,pstc_route_output=0.002,neurons_gate=25,
               route_scale=1,pstc_input=0.01):
        D=self.bg.rules.rule_count
        
        self.bias=self.net.make_input('bias',[1])
        self.rules=self.net.make_array('rules',rule_neurons,D,intercept=(rule_threshold,1),encoders=[[1]],quick=True)
        self.net.connect(self.bias,self.rules)



        self.net.network.exposeOrigin(self.rules.getOrigin('X'),'rules')

        if mutual_inhibit>0:
            self.net.connect(self.rules,self.rules,(numeric.eye(D)-1)*mutual_inhibit,pstc=pstc_inhibit)

        spa.view.rule_watch.add(self.net.network,self.bg.rules.names)


    def connect(self):
        o,t=self.net.connect(self.bg.net.network.getOrigin('output'),self.rules,
                        weight=self.get_param('bg_output_weight'),create_projection=False,pstc=self.p.pstc_input)
        self.net.network.exposeTermination(t,'bg')
        self.spa.net.network.addProjection(self.bg.net.network.getOrigin('output'),self.net.network.getTermination('bg'))

        self.bg.rules.initialize(self.spa)
        for name,source in self.spa.sinks.items():
            t=self.bg.rules.rhs_direct(name)
            if t is not None:
                self.spa.connect_to_sink(self.net.network.getOrigin('rules'),
                                         name,t,self.get_param('pstc_output'))

        for source_name,sink_name,weight in self.bg.rules.get_rhs_routes():
            t=self.bg.rules.rhs_route(source_name,sink_name,weight)

            gname='gate_%s_%s'%(source_name,sink_name)
            if weight!=1: gname+='(%1.1f)'%weight
            gate=self.net.make(gname,self.p.neurons_gate,1,
                               quick=True,encoders=[[1]],intercept=(0.3,1))
            self.net.connect(self.rules,gate,transform=t,pstc=self.p.pstc_to_gate)
            self.net.connect(self.bias,gate)

            source=self.spa.sources[source_name]
            sink=self.spa.sinks[sink_name]
            cname='channel_%s_%s'%(source_name,sink_name)
            if weight!=1: cname+='(%1.1f)'%weight
            channel=self.net.make(cname,self.p.N_per_D*sink.dimension,sink.dimension,quick=True)
            self.net.network.exposeOrigin(channel.getOrigin('X'),cname)
            
            self.spa.connect_to_sink(self.net.network.getOrigin(cname),sink_name,None,
                                     self.p.pstc_output,termination_name=cname)

            o1,t1=self.net.connect(source,channel,pstc=self.p.pstc_route_input,weight=weight*self.p.route_scale,create_projection=False)
            self.net.network.exposeTermination(t1,cname)
            self.spa.net.network.addProjection(o1,self.net.network.getTermination(cname))
            
            channel.addTermination('gate',[[-10.0]]*channel.neurons,self.p.pstc_gate,False)
            self.net.connect(gate,channel.getTermination('gate'))

        """

        # route from a source to a sink, convolving with another source
        for k1,k2,k3 in self.bg.rules._rhs_route_conv2_keys():
            t=self.bg.rules._make_rhs_route_transform(k1,k2,k3)

            gate=net.make('gate_%s_%s_%s'%(k1,k2,k3),25,1,quick=True,encoders=[[1]],intercept=(0.3,1))
            net.connect(self.rules,gate,transform=t,pstc=self.pstc_to_gate)
            net.connect(self.bias,gate)

            if k2.startswith('~'):
                k2=k2[1:]
                invert_second=True
            else:
                invert_second=False

            if k1.startswith('~'):
                k1=k1[1:]
                invert_first=True
            else:
                invert_first=False

            source1=nca._sources[k1]
            source2=nca._sources[k2]
            cname='conv_%s_%s'%(k1,k2)
            vocab=nca.vocab(k3)

            conv=nef.convolution.DirectConvolution(cname,vocab.dimensions,invert_first=invert_first,invert_second=invert_second)
            #TODO: add option to use real convolution instead of direct
            
            net.add(conv)
            net.connect(gate,conv.getTermination('gate'))
            net.network.exposeOrigin(conv.getOrigin('C'),cname)
            net.network.exposeTermination(conv.getTermination('A'),cname+'1')
            net.network.exposeTermination(conv.getTermination('B'),cname+'2')
            nca._net.network.addProjection(source1,net.network.getTermination(cname+'1'))
            nca._net.network.addProjection(source2,net.network.getTermination(cname+'2'))
            nca.connect_to_sink(self.getOrigin(cname),k3,None,self.pstc_output)        
        """

        
    