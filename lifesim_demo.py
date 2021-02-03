import lifesim as ls

# create bus
bus = ls.Bus()

# setting the options
bus.data.options.set_scenario('baseline')

# set options manually
bus.data.options.set_manual(diameter=4.)

# loading and preparing the catalog
bus.data.catalog_from_ppop(input_path='/home/felix/Documents/MA/lifeOS/Data/baselineSample.fits')
bus.data.catalog_remove_distance(stype=0, mode='larger', dist=0.)
bus.data.catalog_remove_distance(stype=4, mode='larger', dist=10.)

# create modules and add to bus
inst = ls.Instrument(name='inst')
bus.add_module(inst)

transm = ls.TransmissionMap(name='transm')
bus.add_module(transm)

exo = ls.PhotonNoiseExozodi(name='exo')
bus.add_module(exo)
local = ls.PhotonNoiseLocalzodi(name='local')
bus.add_module(local)
star = ls.PhotonNoiseStar(name='star')
bus.add_module(star)

# connect all modules
bus.connect(('inst', 'transm'))
bus.connect(('inst', 'exo'))
bus.connect(('inst', 'local'))
bus.connect(('inst', 'star'))

bus.connect(('star', 'transm'))


# run simulation
inst.get_snr()

# optimizing the result
opt = ls.Optimizer(name='opt')
bus.add_module(opt)
ahgs = ls.AhgsModule(name='ahgs')
bus.add_module(ahgs)

bus.connect(('transm', 'opt'))
bus.connect(('inst', 'opt'))
bus.connect(('opt', 'ahgs'))

opt.ahgs()

bus.data.export_catalog(output_path='/home/felix/Documents/MA/Outputs/LIFEsim_development/'
                                    'Test_1.hdf5')