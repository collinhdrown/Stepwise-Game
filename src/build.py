#!/usr/bin/env python3
"""Builds the playable pages from template.html by embedding the dictionary,
start words and bonus-category word lists.

  python3 src/build.py   ->  writes index.html (main layout) and classic.html
                             (ladder-on-the-right layout) in the repository root
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DICT = set(open(os.path.join(HERE, "data/enable1.txt")).read().split())
COMMON = open(os.path.join(HERE, "data/google-10000-english-usa-no-swears.txt")).read().split()

MIN_LEN, MAX_LEN = 3, 15
WORDS = sorted(w for w in DICT if MIN_LEN <= len(w) <= MAX_LEN and re.fullmatch(r"[a-z]+", w))
WSET = set(WORDS)

CATEGORIES = {
    "animal": """
ant ape asp bat bear bee beetle bison boar buck bull calf camel cat cobra cod colt cow coyote crab crane crow cub
deer doe dog donkey dove duck eagle eel elk emu ewe falcon fawn ferret finch fish flea fly foal fox frog gecko gnat
gnu goat goose gopher gorilla hare hawk hen heron hog horse hound hyena ibis jackal jay kid kitten koala lamb lark
leech lemur lion llama lobster louse lynx mare marten mink mole moose moth mouse mule newt orca otter owl ox oyster
panda parrot pig pigeon pony poodle puma pup puppy python quail rabbit ram rat raven rhino robin seal shark sheep
shrew shrimp skunk sloth slug snail snake sow spider squid stag steer stoat stork swan tapir tern tick tiger toad
trout tuna turkey turtle viper vole wasp weasel whale wolf worm wren yak zebra hornet bunny lizard monkey kiwi
dingo hippo owlet egret gull loon boa roach mite grub larva bass carp perch pike sole ray hake ling dace bream
smelt minnow salmon squab drake gander filly steed nag bronco cur mutt pooch tabby beaver badger hamster gerbil
chipmunk squirrel raccoon possum opossum walrus manatee dolphin porpoise jaguar leopard cheetah panther cougar
ocelot bobcat mongoose meerkat aardvark anteater armadillo antelope gazelle impala ibex oryx eland kudu buffalo
chimp baboon gibbon loris ostrich rhea penguin puffin pelican macaw toucan sparrow thrush starling magpie rook kite
osprey vulture condor teal mallard grebe skua petrel albatross midge weevil cricket locust mantis earwig termite
aphid hare mole asp adder krait mamba iguana caiman gator alligator crocodile tortoise terrapin toad salamander
kangaroo wallaby wombat platypus possum mice geese oxen wolves calves sheep deer moose fish lice dodo yeti
bison hen rooster chick chicken cockerel pullet capon turkey drone queen larva pupa grizzly polar elephant
giraffe camel dromedary alpaca vicuna mustang stallion gelding pony mare burro ass hinny zebu yak gaur hart hind
roe fawn buck stag elk caribou reindeer marmot beaver otter mink sable ermine weasel ferret polecat badger
""",
    "food": """
apple bread cake rice bean pea corn meat beef pork ham egg milk cheese butter cream honey jam soup stew pie tart
bun roll toast pasta noodle pizza taco salad fruit grape lemon lime melon peach pear plum berry cherry date fig
kiwi mango olive onion leek kale beet yam potato tomato carrot radish celery pepper garlic ginger herb mint basil
sage thyme salt sugar flour oat bran wheat barley rye nut almond pecan walnut cashew candy fudge toffee cookie
biscuit muffin scone bagel donut waffle crepe pancake omelet bacon sausage steak chop roast veal lamb mutton
venison chicken turkey fish tuna salmon trout cod crab prawn shrimp lobster clam oyster mussel squid sushi curry
chili soy tofu miso broth gravy sauce salsa dip relish pickle chutney mustard ketchup vinegar oil lard tea coffee
cocoa juice cider wine beer ale mead rum gin sake soda lettuce cabbage spinach squash pumpkin turnip parsnip okra
chard endive cress sprout lentil grain cereal porridge gruel granola yogurt custard pudding jelly mousse sorbet
gelato icing frosting syrup treacle caramel nougat praline truffle brownie strudel pastry dumpling ravioli lasagna
gnocchi risotto paella burrito nacho tamale kebab gyro falafel hummus pita naan pretzel cracker wafer chip fries
burger hotdog sandwich sub wrap pesto ragout chowder bisque gumbo jerky salami bologna pastrami brisket rib ribs
cutlet fillet filet loin sirloin mince patty meatball egg yolk tamarind papaya guava lychee banana orange apricot
nectarine quince raisin prune currant melon citrus berry cranberry blueberry raspberry strawberry coconut peanut
pistachio hazelnut chestnut macaroni spaghetti linguine penne bean beans peas chive dill fennel cumin clove
nutmeg cinnamon vanilla anise saffron paprika oregano parsley cilantro scallion shallot tater spud
""",
    "body": """
arm leg hand foot head neck back hip knee toe heel shin calf thigh chin cheek jaw lip mouth nose eye ear brow
lash lid hair skin bone rib spine skull brain heart lung liver kidney gut belly navel waist chest breast palm
wrist elbow finger thumb nail ankle sole arch tooth teeth gum tongue throat larynx scalp temple forehead nape
shoulder armpit fist knuckle joint vein artery nerve muscle tendon colon bowel spleen gland pore cell blood torso
trunk loin limb pelvis tibia femur ulna radius sternum iris pupil retina cornea lobe nostril eyelid eyebrow shank
hock haunch rump butt feet bicep biceps tricep triceps abs gums palate uvula tonsil marrow cartilage ligament
lap instep sinew hamstring shoulder cranium mandible jowl dimple freckle mole wart beard mustache whisker
""",
    "nature": """
tree leaf bush shrub grass moss fern vine weed flower rose lily daisy tulip iris lotus orchid poppy violet petal
seed root stem bark bough twig branch log oak elm ash pine fir yew maple birch cedar willow palm reed rush sedge
forest wood woods grove glade meadow field plain prairie steppe tundra desert dune oasis hill mound mountain
mount peak cliff crag ridge slope valley vale dale glen gorge canyon ravine cave cavern rock stone pebble
boulder sand soil mud clay dust dirt river stream creek brook rill pond lake lagoon sea ocean bay cove gulf
strait marsh swamp bog fen delta island isle reef shore coast beach wave tide surf spring geyser glacier ice snow
frost hail sleet rain storm thunder lightning cloud fog mist dew wind gale breeze gust sun moon star sky comet
planet earth dawn dusk sunset sunrise rainbow volcano lava ember fire flame thorn bud bloom blossom acorn cone
heath moor fell knoll butte mesa crater bluff spruce larch hemlock aspen poplar alder holly ivy clover thistle
nettle heather lichen algae kelp coral shell pearl cloud gully inlet fjord rapids falls torrent puddle
""",
    "clothing": """
hat cap beret beanie hood scarf shawl cape cloak coat jacket parka blazer vest shirt blouse tee top tunic sweater
jumper cardigan dress gown skirt kilt sari robe smock apron pants jeans slacks shorts trousers leggings tights
sock hose stocking shoe boot sandal slipper loafer clog sneaker pump mitt mitten glove belt sash tie bow collar
cuff sleeve pocket button zipper bra slip brief boxer thong bikini toga turban veil mask bonnet helmet visor wig
poncho tuxedo suit uniform overalls bib jersey hoodie sweatshirt pajamas pyjamas nightie garter corset bodice tutu
lei ring watch bangle bracelet necklace earring brooch pendant locket tiara crown purse bag wallet tote satchel
fedora bowler derby stetson sombrero fez turban toque hijab burka sarong caftan kimono dhoti lungi muumuu frock
camisole halter tank smoking anorak mackintosh raincoat trench duster sandals heels flats mules espadrille wader
galosh spat spats bootee diaper nappy shroud cowl wimple stole boa muff earmuff goggles monocle spectacles
""",
    "job": """
baker cook chef maid nurse doctor vet judge clerk agent actor actress artist author poet singer dancer pilot
sailor soldier guard guide coach tutor teacher dean scout spy thief cop sheriff mayor king queen prince duke earl
lord lady monk nun priest pope rabbi imam vicar friar bishop cardinal miner farmer rancher grocer butcher barber
tailor weaver potter smith mason builder plumber painter writer editor banker broker lawyer coder nanny waiter
usher porter valet butler driver rider jockey racer boxer diver skier golfer umpire referee pirate knight squire
page herald jester bard minstrel chemist medic surgeon dentist clown magician wizard witch sage seer captain mate
cadet ensign major colonel general admiral emperor tsar czar sultan khan pharaoh chief boss manager intern
trainee cashier teller typist sculptor glazier roofer joiner carpenter cooper tanner cobbler hatter draper
vendor dealer trader merchant clerk reeve bailiff warden ranger forester herder shepherd drover groom maid
steward hostess host critic pundit scribe sexton deacon pastor cantor mufti lama guru yogi nurse doula midwife
chauffeur courier postman mailman milkman fireman marine ranger sentry warrior archer gunner sniper sergeant
lieutenant corporal private hunter angler fisher whaler trapper logger sawyer navvy cabbie barman barmaid
""",
    "color": """
red blue green yellow orange purple pink brown black white gray grey tan teal cyan aqua navy beige ivory cream gold
silver bronze copper amber ruby jade lime olive plum rose rust scarlet crimson maroon violet indigo lilac lavender
mauve magenta khaki ochre umber sepia coral peach salmon taupe ebony azure cobalt sapphire emerald cerise fuchsia
mint sage tawny russet auburn blond blonde ash slate charcoal pearl lemon mustard burgundy claret wine cherry
tangerine apricot turquoise chartreuse vermilion carmine puce ecru buff fawn dun roan sable jet hazel
""",
    "home": """
bed sofa couch chair stool table desk lamp rug mat bath sink tub tap oven stove fridge pan pot cup mug jug bowl dish
plate fork knife spoon tray vase clock bell door gate wall roof floor stair window shelf rack hook peg pin box bin
can jar lid cork bottle glass towel sheet quilt pillow blanket mirror broom mop brush comb soap sponge bucket pail
kettle toaster blender radio phone bench cabinet closet drawer dresser crib cot hammock candle curtain blind shade
fan heater key lock latch hinge knob plug cord rope string tape glue nail screw basket hamper iron sieve whisk
ladle grater teapot cushion duvet mattress cup saucer platter napkin doormat rug tile sofa futon
""",
    "sport": """
golf polo judo karate tennis squash rugby soccer hockey cricket chess darts bowls boxing fencing archery rowing
sailing skiing surfing diving cycling racing running jogging hiking climbing skating curling lacrosse baseball
football netball handball softball volleyball badminton snooker pool billiards bingo poker bridge rummy cards dice
tag catch hopscotch marbles yoga sumo wrestling biking triathlon marathon sprint relay hurdles javelin discus vault
slalom luge bobsled ball bat club racket puck goal net hoop croquet bowling karting tug jacks checkers draughts
""",
    "feeling": """
joy glee fun love hate fear rage ire anger grief woe sorrow sad happy glad mad calm awe envy pride shame guilt hope
dread angst bliss ennui panic worry alarm cheer mirth delight elation pity scorn spite lust zeal zest boredom
relief shock surprise trust doubt jealousy anxiety stress gloom misery agony pain ache longing yearning nostalgia
regret remorse content tense angry upset afraid scared brave bored lonely jolly merry sulky moody grumpy cross weary
tired hurt peeved irate livid elated proud smug shy timid nervous eager keen giddy sore blue down fond
""",
    "transport": """
car bus van cab taxi truck lorry train tram metro subway bike cycle moped scooter jeep limo coach wagon cart sled
sleigh boat ship yacht canoe kayak raft ferry barge tug liner ark sub plane jet glider blimp rocket shuttle copter
tractor tank trailer camper caravan carriage buggy chariot rickshaw gondola punt dinghy skiff sloop junk dhow
cutter frigate cruiser airship balloon tandem trike unicycle hearse ambulance bulldozer motorbike streetcar trolley
""",
    "tool": """
axe saw drill hammer mallet chisel file rasp plane lathe vise vice wrench spanner pliers tongs clamp level ruler
awl auger bit blade knife shears scissors snips hoe rake spade shovel fork trowel scythe sickle hatchet pick mattock
crowbar lever pulley jack winch hook needle pin thimble loom spindle anvil forge bellows hose ladder sander router
grinder brush roller funnel scraper sword spear lance bow arrow dagger club mace pike gun rifle pistol cannon shield
sling whip trap net rod reel
""",
    "music": """
song tune hymn aria ode opera band choir drum flute fife horn tuba harp lute lyre oboe bass cello viola violin
fiddle piano organ banjo bugle cornet trumpet trombone guitar ukulele sitar zither kazoo gong cymbal bell chime
triangle xylophone sax clarinet bassoon piccolo harmonica accordion bagpipe note chord scale key beat rhythm tempo
melody harmony lyric verse chorus refrain riff solo duet trio quartet jazz blues rock pop rap folk punk soul funk
disco reggae swing gospel ballad anthem carol lullaby dirge march waltz tango samba salsa polka jig reel sonata
concerto symphony overture prelude encore
""",
    "place": """
home house hut shack cabin cottage villa manor palace castle fort tower temple church chapel abbey mosque shrine barn
shed stable farm mill school college library museum gallery theater theatre cinema arena stadium gym pool park zoo
garden yard court mall market shop store bank hotel motel inn pub bar cafe diner bistro bakery office factory plant
depot station port harbor dock pier airport hospital clinic prison jail city town village hamlet capital suburb
street road lane avenue alley plaza square bridge tunnel dam lodge hostel tavern salon studio attic cellar loft
garage porch hall kitchen pantry den lobby foyer ward camp base
""",
}
CATEGORIES = {k: sorted(set(v.split())) for k, v in CATEGORIES.items()}


def expand(words):
    out = set()
    for w in words:
        for f in (w, w + "s", w + "es", (w[:-1] + "ies") if w.endswith("y") else None):
            if f and f in WSET:
                out.add(f)
    return sorted(out)


cats = {k: expand(v) for k, v in CATEGORIES.items()}
missing = {k: [w for w in v if w not in WSET] for k, v in CATEGORIES.items()}


def neighbors(w):
    r, n = set(), len(w)
    for i in range(n):
        s = w[:i] + w[i + 1:]
        r.add(s)
        for j in range(n):
            r.add(s[:j] + w[i] + s[j:])
    for i in range(n):
        for j in range(i + 1, n):
            l = list(w); l[i], l[j] = l[j], l[i]; r.add("".join(l))
    r.discard(w)
    return [x for x in r if x in WSET]


START_LEN = 4
BLOCK = {"texas", "texts"}
starts = []
for w in COMMON[:6000]:
    if len(w) == START_LEN and w in WSET and not w.endswith("s") and w not in BLOCK and len(neighbors(w)) >= 2:
        starts.append(w)

data = {"words": " ".join(WORDS), "starts": starts, "cats": cats}
tpl = open(os.path.join(HERE, "template.html")).read()
html = tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
# Two layouts from one template:
#   index.html   - main layout: recent words and bonuses in the right column
#   classic.html - full ladder in the right column, bonuses below the game
ROOT = os.path.dirname(HERE)
# The template is a page body; give standalone hosting a proper document shell.
# (Head-only tags at the top of the template stay in <head> under HTML parsing rules.)
SHELL = ('<!doctype html>\n<html lang="en" data-theme="organic">\n<head>\n<meta charset="utf-8">\n'
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
         '<style>body { margin: 0; } [hidden] { display: none !important; }</style>\n')
html = SHELL + html
open(os.path.join(ROOT, "index.html"), "w").write(html.replace('/*__LAYOUT__*/"side"', '"stack"'))
open(os.path.join(ROOT, "classic.html"), "w").write(html.replace('<title>Stepwise</title>', '<title>Stepwise Classic</title>', 1))

print(f"words={len(WORDS)} starts={len(starts)} html={len(html)/1e6:.2f}MB")
for k in cats:
    print(f"  {k}: {len(cats[k])} forms; not in dictionary: {' '.join(missing[k]) or '-'}")
