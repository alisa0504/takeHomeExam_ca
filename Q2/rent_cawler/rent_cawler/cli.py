# coding:utf-8
from .__init__ import main
from address_crawler.config.crawler_map import crawler_map
from itertools import chain
import click


@click.command()
@click.argument("sources", nargs=-1, required=True,
                type=click.Choice(
                    ['ALL',
                     'all',
                     *list(crawler_map.keys()),
                     *[k.lower() for k in crawler_map.keys()],
                     ]))
def get_crawlerList(sources):

    click.echo('\n### CLI Options ###\n')
    click.echo(f'sources: {sources}\n')

    main(
        sources=[s.lower() for s in sources]
    )

    return 0


if __name__ == '__main__':
    sys.exit(get_crawlerList())
