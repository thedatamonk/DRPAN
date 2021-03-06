import torch
from torchvision import datasets, transforms
import torchvision.utils as vutils
import torch.utils.data
import torch.backends.cudnn as cudnn

from optparse import OptionParser
import random
import sys

from src.trainer_Stack_pix2pix import GAN_Trainer
from data.dataset import Aligned_Dataset
from utils.tools import get_config

parser = OptionParser()
parser.add_option('--config', type=str, help="net configuration")
parser.add_option('--workers', type=int, help='number of data loading workers', default=2)
parser.add_option('--gpu_ids', default=1, type=int, help='gpu ids: e.g. 0,1,2, 0,2.')
parser.add_option('--manualSeed', type=int, help='manual seed')
# options for different models
# evaluate the models

def main(argv):

    (opt, args) = parser.parse_args(argv)
    config = get_config(opt.config)
    print(opt)
    if opt.manualSeed is None:
        opt.manualSeed = random.randint(1, 10000)
    print("Random Seed: ", opt.manualSeed)
    random.seed(opt.manualSeed)
    torch.manual_seed(opt.manualSeed)
    if config['cuda']:
        torch.cuda.manual_seed_all(opt.manualSeed)
        torch.cuda.set_device(opt.gpu_ids)
    cudnn.benchmark = True

    transform = transforms.Compose([transforms.Resize((512, 512)),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))])
    dataset = Aligned_Dataset(config['datapath'], subfolder='test', direction='AtoB', transform=transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=1,
                                             shuffle=False, num_workers=int(2))
    model_dir = '/media/scw4750/AIwalker/stackgan-like/checkpoints/generator_epoch_160.pkl'
    trainer = GAN_Trainer(config, dataloader)
    # load the model
    trainer.G.load_state_dict(torch.load(model_dir))
    trainer.test()

    return

if __name__ == '__main__':
    main(sys.argv)


