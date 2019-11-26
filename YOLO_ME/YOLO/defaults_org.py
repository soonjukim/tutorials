
class argHandler(dict):
    #A super duper fancy custom made CLI argument handler!!
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    _descriptions = {'help, --h, -h': 'show this super helpful message and exit'}

    def setDefaults(self):
        self.define('imgdir', './data/JPEGImages/', 'path to testing directory with images')
        self.define('binary', './bin/', 'path to .weights directory')
        self.define('config', '../../cfg/', 'path to .cfg directory')
        self.define('dataset', '../../data/JPEGImages/', 'path to dataset directory')
        self.define('labels', '', 'path to labels file')
        self.define('backup', './YOLO/net/ckpt/', 'path to backup folder')
        self.define('summary', '', 'path to TensorBoard summaries directory')
        self.define('annotation', '../../data/Annotations/', 'path to annotation directory')
        self.define('threshold', 0.3, 'detection threshold')
        self.define('model', '../../cfg/yolov2_voc.cfg', 'configuration of choice')
        self.define('trainer', 'rmsprop', 'training algorithm')
        self.define('momentum', 0.0, 'applicable for rmsprop and momentum optimizers')
        self.define('train', True, 'train the whole net')
        self.define('savepb', True, 'train the whole net')
        self.define('load', './bin/yolov2_voc.weights', 'how to initialize the net? Either from .weights')
        self.define('lr', 1e-5, 'learning rate')
        self.define('keep', 20,'Number of most recent training results to save')
        self.define('batch', 16, 'batch size')
        self.define('epoch', 2, 'number of epoch') # 100

    def define(self, argName, default, description):
        self[argName] = default
        self._descriptions[argName] = description
    
    def help(self):
        print('Example usage: first modify the relative directories to the absolute directories in setDefaults()')
        print('Example usage: build --model cfg/yolo.cfg --load bin/yolov2.weights --train')
        print('')
        print('Arguments:')
        spacing = max([len(i) for i in self._descriptions.keys()]) + 2
        for item in self._descriptions:
            currentSpacing = spacing - len(item)
            print('  --' + item + (' ' * currentSpacing) + self._descriptions[item])
        print('')
        exit()

    def parseArgs(self, args):
        print('')
        i = 1
        while i < len(args):
            if args[i] == '-h' or args[i] == '--h' or args[i] == '--help':
                self.help() # Time for some self help! :)
            if len(args[i]) < 2:
                print('ERROR - Invalid argument: ' + args[i])
                print('Try running flow --help')
                exit()

            argumentName = args[i][2:]
            if isinstance(self.get(argumentName), bool):
                if not (i + 1) >= len(args) and (args[i + 1].lower() != 'false' and args[i + 1].lower() != 'true') and not args[i + 1].startswith('--'):
                    print('ERROR - Expected boolean value (or no value) following argument: ' + args[i])
                    print('Try running flow --help')
                    exit()
                elif not (i + 1) >= len(args) and (args[i + 1].lower() == 'false' or args[i + 1].lower() == 'true'):
                    self[argumentName] = (args[i + 1].lower() == 'true')
                    i += 1
                else:
                    self[argumentName] = True
            elif args[i].startswith('--') and not (i + 1) >= len(args) and not args[i + 1].startswith('--') and argumentName in self:
                if isinstance(self[argumentName], float):
                    try:
                        args[i + 1] = float(args[i + 1])
                    except:
                        print('ERROR - Expected float for argument: ' + args[i])
                        print('Try running flow --help')
                        exit()
                elif isinstance(self[argumentName], int):
                    try:
                        args[i + 1] = int(args[i + 1])
                    except:
                        print('ERROR - Expected int for argument: ' + args[i])
                        print('Try running flow --help')
                        exit()
                self[argumentName] = args[i + 1]
                i += 1
            else:
                print('ERROR - Invalid argument: ' + args[i])
                print('Try running flow --help')
                exit()
            i += 1
